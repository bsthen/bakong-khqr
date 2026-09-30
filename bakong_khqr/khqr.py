# bakong_khqr/khqr.py

import time
import json
import warnings
import http.client
from typing import Any, Union
from urllib.parse import urlparse
from contextlib import closing

from .sdk.crc import CRC
from .sdk.mcc import MCC
from .sdk.hash import HASH
from .sdk.amount import Amount
from .sdk.timestamp import TimeStamp
from .sdk.image_tools import ImageTools
from .sdk.country_code import CountryCode
from .sdk.merchant_city import MerchantCity
from .sdk.merchant_name import MerchantName
from .sdk.point_of_initiation import PointOfInitiation
from .sdk.transaction_currency import TransactionCurrency
from .sdk.additional_data_field import AdditionalDataField
from .sdk.payload_format_indicator import PayloadFormatIndicator
from .sdk.global_unique_identifier import GlobalUniqueIdentifier

from .sdk.version import __version__


class KHQRResponse(str):
    """
    An enhanced KHQR string response that seamlessly inherits from Python's built-in `str`.
    
    It maintains 100% backward compatibility by acting directly as the raw KHQR string 
    (e.g., in print(), len(), slicing, or passing to qr_image()), while simultaneously 
    exposing all metadata returned by the KHQR.dev API server:

    Attributes:
        qr (str): The raw EMVCo KHQR code string.
        md5 (str | None): The 32-character MD5 checksum hash.
        tran_id (str | None): Unique transaction / bill tracking identifier.
        checkout_url (str | None): The Web Checkout URL (None if URLs omitted or unverified).
        raw (dict): The complete raw JSON response returned by the server.
    """
    qr: str
    md5: str | None
    tran_id: str | None
    checkout_url: str | None
    raw: dict[str, Any]

    def __new__(
        cls,
        qr: str,
        md5: str | None = None,
        tran_id: str | None = None,
        checkout_url: str | None = None,
        raw: dict[str, Any] | None = None
    ):
        instance = super().__new__(cls, qr)
        instance.qr = qr
        instance.md5 = md5
        instance.tran_id = tran_id
        instance.checkout_url = checkout_url
        instance.raw = raw or {}
        return instance

    def get(self, key: str, default: Any = None) -> Any:
        """Allow dict-like access via .get(key)."""
        if hasattr(self, key):
            val = getattr(self, key)
            if val is not None:
                return val
        data = self.raw.get("data")
        if isinstance(data, dict) and key in data:
            return data[key]
        return self.raw.get(key, default)

    def __getitem__(self, item: Any) -> Any:
        """Allow dict-like subscription (e.g. res['checkout_url']) while preserving str slicing."""
        if isinstance(item, str):
            if item in ("qr", "md5", "tran_id", "checkout_url"):
                return getattr(self, item)
            data = self.raw.get("data")
            if isinstance(data, dict) and item in data:
                return data[item]
            if item in self.raw:
                return self.raw[item]
            raise KeyError(item)
        return super().__getitem__(item)

    def to_dict(self) -> dict[str, Any]:
        """Convert the response object to a standard Python dictionary."""
        return {
            "qr": self.qr,
            "md5": self.md5,
            "tran_id": self.tran_id,
            "checkout_url": self.checkout_url
        }


class KHQR:
    def __init__(self, bakong_token: str | None = None):
        self.__crc = CRC()
        self.__mcc = MCC()
        self.__hash = HASH()
        self.__amount = Amount()
        self.__timestamp = TimeStamp()
        self.__image_tools = ImageTools()
        self.__country_code = CountryCode()
        self.__merchant_city = MerchantCity()
        self.__merchant_name = MerchantName()
        self.__point_of_initiation = PointOfInitiation()
        self.__transaction_currency = TransactionCurrency()
        self.__additional_data_field = AdditionalDataField()
        self.__payload_format_indicator = PayloadFormatIndicator()
        self.__global_unique_identifier = GlobalUniqueIdentifier()
        self.__bakong_token = bakong_token.strip() if bakong_token else None

        # ⚡️ ភ្ជាប់ទៅកាន់ Endpoint ថ្មី api.khqr.dev/v1
        if self.__bakong_token and self.__bakong_token.startswith("rbk"):
            self.__bakong_api = "https://api.khqr.dev/v1"
            self.__is_relay = True
        else:
            self.__bakong_api = "https://api-bakong.nbc.gov.kh/v1"
            self.__is_relay = False
    
    def __check_relay_token(self):
        """Helper method to ensure the token is a Relay token."""
        if not self.__bakong_token or not self.__bakong_token.startswith("rbk"):
            raise ValueError("A valid Relay Token (starting with 'rbk') is required to use Relay features.")
        
    def __check_bakong_token(self):
        if not self.__bakong_token:
            raise ValueError("Developer Token is required for KHQR class initialization. Example usage: khqr = KHQR('your_token_here').")

    def __post_request(self, endpoint: str, payload: dict[str, Any] | list[Any]) -> dict[str, Any]:
        self.__check_bakong_token()
        
        parsed_url = urlparse(self.__bakong_api)
        with closing(http.client.HTTPSConnection(parsed_url.netloc, timeout=12)) as conn:
            headers = {
                "Authorization": f"Bearer {self.__bakong_token}",
                "Content-Type": "application/json",
                "User-Agent": f"bakong-khqr/{__version__} (+https://github.com/bsthen/bakong-khqr)"
            }

            full_path = f"{parsed_url.path}{endpoint}".replace("//", "/")
            
            try:
                conn.request("POST", full_path, body=json.dumps(payload), headers=headers)
                response = conn.getresponse()
                response_data = response.read().decode("utf-8")
            except TimeoutError:
                target = "KHQR.dev API" if self.__is_relay else "Bakong API"
                raise ValueError(f"{target} took too long to respond. Please check transaction status later.")
            except Exception as e:
                target = "KHQR.dev API" if self.__is_relay else "Bakong API"
                raise ValueError(f"Failed to connect to {target}: {e}")

            if response.status in (200, 201):
                try:
                    data = json.loads(response_data)
                    if not isinstance(data, dict):
                        raise ValueError("API returned valid JSON but it is not a dictionary.")
                    return data
                except json.JSONDecodeError:
                    raise ValueError(f"Server returned invalid JSON: {response_data}")
            
            if self.__is_relay:
                try:
                    error_data = json.loads(response_data)
                    if isinstance(error_data, dict):
                        err_code = error_data.get("errorCode")
                        err_msg = error_data.get("responseMessage", "")

                        if endpoint == "/check_transaction_by_md5" and (response.status == 404 or (response.status == 400 and err_code == 3)):
                            return error_data

                        if response.status == 401 or err_code == 6:
                            raise ValueError(f"Unauthorized: {err_msg or 'Token is missing, expired, invalid, or has reached its usage limit.'}")
                        elif response.status == 429 or err_code == 429:
                            raise ValueError(f"Rate limit exceeded: {err_msg}")
                        elif response.status == 503 or err_code == 99:
                            raise ValueError(f"Service maintenance: {err_msg or 'Service is currently undergoing maintenance.'}")
                        elif err_code == 10:
                            raise ValueError(f"Store Configuration Error: {err_msg}")
                        elif err_code == 14:
                            raise ValueError(f"Validation Error: {err_msg}")
                        elif err_msg:
                            raise ValueError(err_msg)
                except json.JSONDecodeError:
                    pass

                relay_errors = {
                    400: "Bad request to KHQR.dev. Please check your parameters.",
                    401: "Unauthorized: Token is missing, expired, invalid, or has reached its usage limit.",
                    429: "Too many requests to KHQR.dev. Please wait before trying again.",
                    500: "KHQR.dev encountered an internal server error.",
                    503: "KHQR.dev is currently undergoing maintenance. Please try again shortly."
                }
                raise ValueError(relay_errors.get(response.status, f"HTTP {response.status}: {response_data}"))

            try:
                error_data = json.loads(response_data)
                if isinstance(error_data, dict) and "responseCode" in error_data:
                    return error_data
            except json.JSONDecodeError:
                pass
            
            errors = {
                400: "Bad request. Please check your input parameters and try again.",
                401: "Your Developer Token is either incorrect or expired. Please renew it through Bakong Developer.",
                403: "Bakong API only accepts requests from Cambodia IP addresses. Your IP may be blocked or restricted.",
                404: "The requested Bakong API endpoint does not exist. Please check the endpoint URL.",
                429: "Too many requests. Please wait a while before trying again.",
                500: "Bakong server encountered an internal error. Please try again later.",
                504: "Bakong server is busy, please try again later."
            }
            
            msg = errors.get(response.status, f"HTTP {response.status}: {response_data}")
            raise ValueError(msg)

    def create_qr(
        self,
        amount: float = 0.0,
        return_url: str | None = None,
        success_url: str | None = None,
        cancel_url: str | None = None,
        account_id: str | None = None,
        merchant_name: str | None = None,
        merchant_city: str | None = None,
        currency: str | None = None,
        store_label: str | None = None,
        phone_number: str | None = None,
        bill_number: str | None = None,
        terminal_label: str | None = None,
        static: bool = False,
        expiration: int = 1,
        return_dict: bool = False,
        **kwargs
    ) -> Union[KHQRResponse, dict[str, Any]]:
        """
        Generate a KHQR code transaction string and optional Web Checkout session.

        When using KHQR.dev (`rbk_...` token), merchant account information and currency 
        are automatically derived from the store's configured payment link. Only `amount` 
        is mandatory.

        Args:
            amount (float | int): **[Required]** Transaction amount to collect (e.g. 10.0 or 15000).
                Minimum for USD is 0.01; Minimum for KHR is 100.
            return_url (str, optional): Default redirect destination URL after payment 
                completion or cancellation. Must match your store's verified domain.
            success_url (str, optional): Target destination URL specifically on successful 
                payment completion. Must match your store's verified domain.
            cancel_url (str, optional): Target destination URL if user cancels or session expires.
                Must match your store's verified domain.
            account_id (str, optional): The recipient Bakong Account ID (e.g., 'your_name@bank').
                Required for standard NBC tokens; Optional/Deprecated for Relay tokens.
            merchant_name (str, optional): Merchant display name.
                Required for standard NBC tokens; Optional/Deprecated for Relay tokens.
            merchant_city (str, optional): Merchant operating city (e.g., 'Phnom Penh').
                Required for standard NBC tokens; Optional/Deprecated for Relay tokens.
            currency (str, optional): Currency code ('USD' or 'KHR').
                Required for standard NBC tokens; Optional/Deprecated for Relay tokens.
            store_label (str, optional): Store branch reference or transaction title.
            phone_number (str, optional): Merchant contact phone number.
            bill_number (str, optional): Invoice / Order reference identifier.
            terminal_label (str, optional): POS terminal identifier.
            static (bool): Set to True for static QR (no amount); Defaults to False (Dynamic).
            expiration (int): Expiration time in days (default: 1 day).
            return_dict (bool): Set to True to return a standard dictionary instead of KHQRResponse.
            **kwargs: Backward compatibility arguments (e.g., `bank_account`).

        Returns:
            KHQRResponse | dict:
                An enhanced KHQR string object that behaves as `str` while also exposing:
                - `.qr` : The raw KHQR code string.
                - `.md5` : The 32-character MD5 checksum hash.
                - `.tran_id` : The purchase transaction identifier.
                - `.checkout_url` : The hosted Web Checkout link (if redirect URLs are provided).
                If `return_dict=True`, returns the raw JSON dictionary.
        """
        if "bank_account" in kwargs:
            warnings.warn(
                "The 'bank_account' parameter is deprecated and will be removed in future versions. "
                "Please use 'account_id' instead.",
                DeprecationWarning,
                stacklevel=2
            )
            if not account_id:
                account_id = kwargs.pop("bank_account")

        # ── ⚡️ ករណីដំណើរការជាមួយ KHQR.dev (api.khqr.dev) ──────────────────────
        if self.__is_relay:
            payload: dict[str, Any] = {
                "amount": float(amount)
            }
            if return_url is not None:
                payload["return_url"] = return_url
            if success_url is not None:
                payload["success_url"] = success_url
            if cancel_url is not None:
                payload["cancel_url"] = cancel_url
            if account_id is not None:
                payload["account_id"] = account_id
            if merchant_name is not None:
                payload["merchant_name"] = merchant_name
            if merchant_city is not None:
                payload["merchant_city"] = merchant_city
            if currency is not None:
                payload["currency"] = currency
            if store_label is not None:
                payload["store_label"] = store_label
            if phone_number is not None:
                payload["phone_number"] = phone_number
            if bill_number is not None:
                payload["bill_number"] = bill_number
            if terminal_label is not None:
                payload["terminal_label"] = terminal_label
            if static:
                payload["static"] = static
            if expiration != 1:
                payload["expiration"] = expiration

            response = self.__post_request("/generate_qr", payload)

            if response.get("responseCode") == 0:
                data = response.get("data")
                if isinstance(data, dict):
                    if return_dict:
                        return response

                    qr_str = str(data.get("qr", ""))
                    return KHQRResponse(
                        qr=qr_str,
                        md5=data.get("md5"),
                        tran_id=data.get("tran_id"),
                        checkout_url=data.get("checkout_url"),
                        raw=response
                    )

            error_msg = response.get("responseMessage", "Failed to generate KHQR via KHQR.dev.")
            raise ValueError(error_msg)

        # ── ករណីដំណើរការជាមួយ NBC Bakong Token ដើម (Offline Local Generation) ───
        if not account_id:
            raise ValueError("Missing required argument: 'account_id'.")
        if not merchant_name:
            raise ValueError("Missing required argument: 'merchant_name'.")
        if not merchant_city:
            raise ValueError("Missing required argument: 'merchant_city'.")
        if not currency:
            raise ValueError("Missing required argument: 'currency'.")
        
        if amount <= 0:
            static = True
        
        qr_data = self.__payload_format_indicator.value()
        qr_data += self.__point_of_initiation.static() if static else self.__point_of_initiation.dynamic()
        qr_data += self.__global_unique_identifier.value(account_id)
        qr_data += self.__mcc.value()
        qr_data += self.__transaction_currency.value(currency)
        if not static:
            qr_data += self.__amount.value(amount)
        qr_data += self.__country_code.value()
        qr_data += self.__merchant_name.value(merchant_name)
        qr_data += self.__merchant_city.value(merchant_city)
        
        additional_data = self.__additional_data_field.value(
            store_label=store_label,
            phone_number=phone_number,
            bill_number=bill_number,
            terminal_label=terminal_label,
        )
        if additional_data:
            qr_data += additional_data
            
        qr_data += self.__timestamp.value(static, expiration)
        qr_data += self.__crc.value(qr_data)
        
        local_md5 = self.__hash.md5(qr_data)

        if return_dict:
            return {
                "responseCode": 0,
                "responseMessage": "KHQR Generated Successfully.",
                "data": {
                    "qr": qr_data,
                    "md5": local_md5,
                    "tran_id": bill_number,
                    "checkout_url": None
                }
            }

        return KHQRResponse(
            qr=qr_data,
            md5=local_md5,
            tran_id=bill_number,
            checkout_url=None,
            raw={
                "responseCode": 0,
                "responseMessage": "Local KHQR Generated",
                "data": {
                    "qr": qr_data,
                    "md5": local_md5,
                    "tran_id": bill_number,
                    "checkout_url": None
                }
            }
        )

    def generate_md5(self, qr: str) -> str:
        """
        Generate an MD5 hash for the QR code.

        This hash is used as a unique identifier to check transaction 
        statuses via the Bakong API.

        Args:
            qr (str): QR code string generated from the `create_qr()` method.

        Returns:
            str: The 32-character MD5 hash string.
        """
        return self.__hash.md5(qr)
    
    def generate_deeplink(
        self, 
        qr: str, 
        appDeepLinkCallback: str | None = None, 
        appIconUrl: str = "https://bakong.nbc.gov.kh/images/logo.svg", 
        appName: str = "MyAppName",
        callback: str | None = None
    ) -> str | None:
        """
        Generate a deep link for the KHQR.

        Args:
            qr (str): QR code string generated from `create_qr()` method.
            appDeepLinkCallback (str, optional): The standard callback URL.
            appIconUrl (str, optional): URL for the app icon.
            appName (str, optional): Name of the application.
            callback (str, optional): Deprecated callback parameter.

        Returns:
            str | None: The generated Bakong short-link URL or None if failed.
        """
        if callback is not None:
            warnings.warn(
                f"\n\n{'!'*31} DEPRECATION WARNING {'!'*31}\n"
                f"Parameter 'callback' is deprecated in bakong-khqr.\n"
                f"Please update your code to use 'appDeepLinkCallback' instead.\n"
                f"{'!'*83}\n",
                DeprecationWarning,
                stacklevel=2
            )
            if appDeepLinkCallback is None:
                appDeepLinkCallback = callback

        if appDeepLinkCallback is None:
            appDeepLinkCallback = "https://bakong.nbc.org.kh"

        payload = {
            "qr": str(qr),
            "sourceInfo": {
                "appIconUrl": appIconUrl,
                "appName": appName,
                "appDeepLinkCallback": appDeepLinkCallback
            }
        }
        
        response = self.__post_request("/generate_deeplink_by_qr", payload)
        
        if response.get("responseCode") == 0:
            data = response.get("data")
            if isinstance(data, dict):
                return data.get("shortLink")
        return None
    
    def check_payment(
        self, 
        md5: str,
        start_time: float | None = None
    ) -> str | tuple[str, int]:
        """
        Check the payment status of a transaction by its MD5 hash.

        Args:
            md5 (str): The MD5 hash of the QR code generated via `generate_md5()`.
            start_time (float, optional): The timestamp (time.time()) when the transaction 
                or QR code was created. If provided, returns a tuple containing the status 
                and the suggested next polling delay in seconds.
            
        Returns:
            str | tuple[str, int]: 
                - If `start_time` is None: Returns status string ('PAID', 'SCANNED', 'EXPIRED', or 'UNPAID').
                - If `start_time` is provided: Returns a tuple `(status, next_delay)` 
                  where `next_delay` is the suggested sleep time in seconds.
        """
        payload = {
            "md5": md5
        }
        
        response = self.__post_request("/check_transaction_by_md5", payload)
        data = response.get("data") if isinstance(response.get("data"), dict) else {}
        resp_code = response.get("responseCode")

        if self.__is_relay:
            raw_status = str(data.get("status", "")).upper()
            raw_tracking = str(data.get("trackingStatus", "")).upper()

            if raw_status == "SCANNED" or raw_tracking == "SCANNED":
                status = "SCANNED"
            elif raw_status == "EXPIRED" or raw_tracking == "EXPIRED":
                status = "EXPIRED"
            elif raw_status == "PAID" or raw_tracking == "SUCCESS":
                status = "PAID"
            elif resp_code == 0:
                status = "PAID"
            else:
                status = "UNPAID"

            if start_time is None:
                return status

            if status in ("PAID", "EXPIRED"):
                return status, 0

            elapsed = time.time() - start_time

            if status == "SCANNED":
                next_delay = 3
            elif elapsed <= 300:
                next_delay = 5
            elif elapsed <= 900:
                next_delay = 10
            elif elapsed <= 3600:
                next_delay = 15
            else:
                next_delay = 300

            return status, next_delay

        if resp_code == 0:
            status = "PAID"
        else:
            status = "UNPAID"
        
        if start_time is None:
            return status

        if status == "PAID":
            return status, 0
            
        elapsed = time.time() - start_time
        
        if elapsed <= 300:
            next_delay = 5
        elif elapsed <= 900:
            next_delay = 10
        elif elapsed <= 3600:
            next_delay = 15
        else:
            next_delay = 300
            
        return status, next_delay
    
    def get_payment(
        self, 
        md5: str
    ) -> dict[str, Any] | None:
        """
        Retrieve details for a specific paid transaction using its MD5 hash.

        Args:
            md5 (str): The MD5 hash of the QR code.
        
        Returns:
            dict[str, Any] | None: A dictionary containing transaction details 
                if the payment is confirmed as PAID. Returns None if the transaction 
                is still pending, scanned, expired, or not found.
        """
        payload = {
            "md5": md5
        }
        
        response = self.__post_request("/check_transaction_by_md5", payload)
        
        if response.get("responseCode") == 0:
            data = response.get("data")
            if isinstance(data, dict):
                if self.__is_relay:
                    status = str(data.get("status", "")).lower()
                    tracking = str(data.get("trackingStatus", "")).upper()
                    if status == "scanned" or tracking == "SCANNED":
                        return None
                return data
        return None
    
    def check_bulk_payments(
        self,
        md5_list: list[str]
    ) -> list[str]:
        """
        Check transaction status for multiple MD5 hashes simultaneously.

        Args:
            md5_list (list[str]): A list of MD5 hashes to verify (max 50).

        Returns:
            list[str]: A list containing only the MD5 hashes of transactions 
                confirmed as paid.
        """
        if len(md5_list) > 50:
            raise ValueError("The md5_list exceeds the allowed limit of 50 hashes per request.")

        response = self.__post_request("/check_transaction_by_md5_list", md5_list)
        
        data_list = response.get("data")
        if not isinstance(data_list, list):
            return []
        
        paid_hashes = []
        for item in data_list:
            if isinstance(item, dict) and item.get("status") in ("SUCCESS", "PAID"):
                md5 = item.get("md5")
                if isinstance(md5, str):
                    paid_hashes.append(md5)
        
        return paid_hashes
    
    def qr_image(
        self, 
        qr: str,
        format: str = "png",
        output_path: str | None = None,
    ) -> str | bytes:
        """
        Generate a styled KHQR image from the QR string.

        Args:
            qr (str): Raw KHQR string.
            format (str): Desired format ('png', 'jpeg', 'webp', 'bytes', 'base64', 'base64_uri').
            output_path (str, optional): Target file path if saving to disk.

        Returns:
            str | bytes: File path, base64 string, or raw bytes depending on chosen format.
        """
        result = self.__image_tools.generate(str(qr))

        if format.lower() in ("jpeg", "jpg"):
            return result.to_jpeg(output_path)
        elif format.lower() == "webp":
            return result.to_webp(output_path)
        elif format.lower() == "bytes":
            return result.to_bytes()
        elif format.lower() == "base64":
            return result.to_base64()
        elif format.lower() == "base64_uri":
            return result.to_data_uri()
        else:
            return result.to_png(output_path)

    # ── ⚡️ DEPRECATED WEB CHECKOUT METHODS ─────────────────────────────────

    def create_webcheckout(
        self,
        trans_id: str | None = None,
        account_id: str | None = None,
        merchant_name: str | None = None,
        merchant_city: str | None = None,
        amount: float = 0.0,
        currency: str | None = None,
        return_url: str | None = None,
        webhook_url: str | None = None,
        lang: str = "km",
        ttl: int = 5,
        **kwargs
    ) -> dict[str, Any]:
        """
        [DEPRECATED] Create a Web Checkout session.

        This method is deprecated since version 0.7.0. Web Checkout creation 
        is now integrated directly into `create_qr()`.

        Example Migration:
        >>> res = khqr.create_qr(amount=10.0, return_url="https://yourstore.com/checkout/return")
        >>> print("Checkout URL:", res.checkout_url)
        """
        warnings.warn(
            "Method 'create_webcheckout' is deprecated and will be removed in a future release. "
            "Please use 'create_qr(amount=..., return_url=...)' instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self.__check_relay_token()

        res = self.create_qr(
            amount=amount,
            return_url=return_url,
            success_url=kwargs.get("success_url"),
            cancel_url=kwargs.get("cancel_url"),
            account_id=account_id,
            merchant_name=merchant_name,
            merchant_city=merchant_city,
            currency=currency,
            bill_number=trans_id,
            return_dict=True
        )
        return res if isinstance(res, dict) else res.raw

    def get_webcheckout(
        self,
        session_id: str
    ) -> dict[str, Any] | None:
        """
        [DEPRECATED] Retrieve transaction details and status of a Web Checkout session.

        This method is deprecated since version 0.7.0. Please use `check_payment(md5)` 
        or `get_payment(md5)` instead.
        """
        warnings.warn(
            "Method 'get_webcheckout' is deprecated. Please use 'check_payment(md5)' or 'get_payment(md5)' instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self.__check_relay_token()
        return self.get_payment(session_id)