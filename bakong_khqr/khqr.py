import time
import json
import warnings
import http.client
from typing import Any
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
        self.__bakong_token = bakong_token
        # Set the API endpoint based on the provided token
        if bakong_token and bakong_token.startswith("rbk"):
            self.__bakong_api = "https://api.bakongrelay.com/v1"
        else:
            self.__bakong_api = "https://api-bakong.nbc.gov.kh/v1"
    
    def __check_relay_token(self):
        """Helper method to ensure the token is a Bakong Relay token."""
        if not self.__bakong_token or not self.__bakong_token.startswith("rbk"):
            raise ValueError("A valid Relay Token (starting with 'rbk') is required to use Web Checkout features.")
        
    def __check_bakong_token(self):
        if not self.__bakong_token:
            raise ValueError("Bakong Developer Token is required for KHQR class initialization. Example usage: khqr = KHQR('your_token_here').")

    def __post_request(self, endpoint: str, payload: dict[str, Any] | list[Any]) -> dict[str, Any]:
        self.__check_bakong_token()
        
        parsed_url = urlparse(self.__bakong_api)
        # Using 'with' or closing ensures the socket closes even if an error occurs
        with closing(http.client.HTTPSConnection(parsed_url.netloc, timeout=10)) as conn:
            headers = {
                "Authorization": f"Bearer {self.__bakong_token}",
                "Content-Type": "application/json",
                "User-Agent": f"bakong-khqr/{__version__} (+https://github.com/bsthen/bakong-khqr)"
            }

            full_path = f"{parsed_url.path}{endpoint}".replace("//", "/")
            
            try:
                conn.request("POST", full_path, body=json.dumps(payload), headers=headers)
                response = conn.getresponse()
                response_data = response.read().decode()
                
            except TimeoutError:
                raise ValueError("Bakong API took too long to respond. Please check transaction status later.")
            
            except Exception as e:
                raise ValueError(f"Failed to connect to Bakong API: {e}")

            if response.status in (200, 201):
                try:
                    data = json.loads(response_data)
                    if not isinstance(data, dict):
                        raise ValueError("API returned valid JSON but it is not a dictionary.")
                    return data
                except json.JSONDecodeError:
                    raise ValueError(f"Bakong returned invalid JSON: {response_data}")
            
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
        account_id: str | None = None,
        merchant_name: str | None = None,
        merchant_city: str | None = None,
        amount: float = 0.0,
        currency: str | None = None,
        store_label: str | None = None,
        phone_number: str | None = None,
        bill_number: str | None = None,
        terminal_label: str | None = None,
        static: bool = False,
        expiration: int = 1,
        **kwargs
    ) -> str:
        """
        Create a KHQR string compliant with the Bakong system.

        Args:
            account_id (str): The recipient Bakong Account ID (e.g., 'your_name@bank').
            merchant_name (str): Name of the merchant (e.g., 'Your Name').
            merchant_city (str): City of the merchant (e.g., 'Phnom Penh').
            amount (float | int): Transaction amount.
            currency (str): Currency code, either 'USD' or 'KHR'.
            store_label (str, optional): Store label or ID.
            phone_number (str, optional): Merchant's mobile number.
            bill_number (str, optional): Unique bill or transaction reference.
            terminal_label (str, optional): Terminal ID or a short description.
            static (bool): Set to **True** for a static QR (no amount); Defaults to **False** (Dynamic).
            expiration (int): Expiration time in days. Defaults to 1 day.
            **kwargs: Used for backward compatibility (e.g., `bank_account`).

        Returns:
            str: A formatted EMVCo-compliant KHQR string.
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
        qr_data += self.__global_unique_identifier.value(account_id)  # <-- ប្តូរមកប្រើ account_id
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
        
        return qr_data

    def generate_md5(
        self, 
        qr: str
        ) -> str:
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
        callback: str | None = None # Deprecated parameter
    ) -> str | None:
        """
        Generate a deep link for the KHQR.

        .. deprecated:: 0.5.7
            The `callback` parameter is deprecated. Use `appDeepLinkCallback` 
            to align with the National Bank of Cambodia (NBC) standard.

        Args:
            qr (str): QR code string generated from `create_qr()` method.
            appDeepLinkCallback (str, optional): The standard callback URL. 
                Defaults to "https://bakong.nbc.org.kh".
            appIconUrl (str, optional): URL for the app icon.
                Defaults to "https://bakong.nbc.gov.kh/images/logo.svg".
            appName (str, optional): Name of the application.
                Defaults to "MyAppName".
            callback (str, optional): **Deprecated alias** for appDeepLinkCallback.

        Returns:
            str | None: The generated Bakong short-link URL or None if failed.
        """

        # Handle Deprecation Logic
        if callback is not None:
            warnings.warn(
                f"\n\n{'!'*31} DEPRECATION WARNING {'!'*31}\n"
                f"Parameter 'callback' is deprecated in bakong-khqr.\n"
                f"Please update your code to use 'appDeepLinkCallback' instead.\n"
                f"Example: deeplink = khqr.generate_deeplink(qr=qr_string, appDeepLinkCallback='...') \n"
                f"{'!'*83}\n",
                DeprecationWarning,
                stacklevel=2
            )
            # Use 'callback' value only if the new param wasn't provided
            if appDeepLinkCallback is None:
                appDeepLinkCallback = callback

        # Set default if neither was provided
        if appDeepLinkCallback is None:
            appDeepLinkCallback = "https://bakong.nbc.org.kh"

        payload = {
            "qr": qr,
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
        start_time: float = None
    ) -> str | tuple[str, int]:
        """
        Check the payment status of a transaction by its MD5 hash.
        Supports smart dynamic polling delays based on the Dynamic Windows Matrix.

        Args:
            md5 (str): The MD5 hash of the QR code generated via `generate_md5()`.
            start_time (float, optional): The timestamp (time.time()) when the transaction 
                                        or QR code was created. If provided, returns a tuple 
                                        containing the status and the suggested next delay.
            
        Returns:
            str | tuple[str, int]: 
                - If `start_time` is None: Returns a string status (`PAID` or `UNPAID`).
                - If `start_time` is provided: Returns a tuple `(status, next_delay)` 
                where `next_delay` is the suggested sleep time in seconds.
        
        Note:
            A status of **UNPAID** may indicate that the transaction is still pending 
            or that the QR code has not been scanned yet.
        """
        
        payload = {
            "md5": md5
        }
        
        # Send request to Bakong Relay API to check transaction status
        response = self.__post_request("/check_transaction_by_md5", payload)
        status = "PAID" if response.get("responseCode") == 0 else "UNPAID"
        
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
            md5 (str): The MD5 hash of the QR code, typically generated 
                via the `generate_md5()` method.
        
        Returns:
            dict[str, Any] | None: A dictionary containing transaction details 
                (e.g., amount, currency, sender) if the payment is successful. 
                Returns `None` if the transaction is pending or not found.
        """
        
        payload = {
            "md5": md5
        }
        
        response = self.__post_request("/check_transaction_by_md5", payload)
        
        if response.get("responseCode") == 0:
            data = response.get("data")
            return data if isinstance(data, dict) else None
        return None
    
    def check_bulk_payments(
        self,
        md5_list: list[str]
    ) -> list[str]:
        """
        Check the transaction status for multiple MD5 hashes.

        Args:
            md5_list (list[str]): A list of MD5 hashes to verify. 
                Each hash should be generated using the `generate_md5()` method.

        Returns:
            list[str]: A list containing only the MD5 hashes of transactions 
                that have been confirmed as paid.

        Raises:
            ValueError: If the `md5_list` contains more than 50 items, 
                as per Bakong's API limits.
        """
        if len(md5_list) > 50:
            raise ValueError("The md5_list exceeds the allowed limit of 50 hashes per request.")

        response = self.__post_request("/check_transaction_by_md5_list", md5_list)
        
        data_list = response.get("data")
        if not isinstance(data_list, list):
            return []
        
        paid_hashes = []
        for item in data_list:
            if isinstance(item, dict) and item.get("status") == "SUCCESS":
                md5 = item.get("md5")
                if isinstance(md5, str):
                    paid_hashes.append(md5)
        
        return paid_hashes
    
    def qr_image(
        self, qr: str,
        format: str = "png",
        output_path: str | None = None,
        ) -> str | bytes:
        """
        Generate a styled KHQR image from the QR string.

        Args:
            qr (str): The KHQR string generated from the `create_qr()` method.
            output_path (str, optional): The file path where the image will be saved. 
                If not provided, the method returns a temporary file path or data.
            format (str): The export format. Supported: 'png', 'jpeg', 'webp', 
                'bytes', 'base64', or 'base64_uri'. Defaults to 'png'.

        Returns:
            str | bytes: The file path (str) if saved to disk, or the raw data 
                (bytes/base64 string) depending on the requested format.

        Raises:
            ImportError: If the required imaging libraries (Pillow/qrcode) are not installed.
            ValueError: If an unsupported format is requested.
        """

        result = self.__image_tools.generate(qr)

        if format.lower() == "jpeg" or format.lower() == "jpg":
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

    def create_webcheckout(
        self,
        trans_id: str,
        account_id: str,
        merchant_name: str,
        merchant_city: str,
        amount: float,
        currency: str,
        return_url: str,
        webhook_url: str,
        lang: str = "km",
        ttl: int = 5
    ) -> dict[str, Any]:
        """
        Create a new Bakong Web Checkout session.
        
        ⚠️ IMPORTANT: The domains for `return_url` and `webhook_url` MUST be whitelisted.
        To whitelist your domains, please use the Telegram Bot: 
        👉 https://t.me/bakong_relay_bot?start=relay_signup

        Args:
            trans_id (str): Your platform's unique transaction or tracking identifier.
            account_id (str): The recipient Bakong Account ID (e.g., merchant@bank).
            merchant_name (str): The display name of the merchant.
            merchant_city (str): The merchant operating city (e.g., 'Phnom Penh').
            amount (float): Total transaction value to collect.
            currency (str): The target currency ('USD' or 'KHR').
            return_url (str): The web destination to send the user after payment.
            webhook_url (str): Server-to-server callback endpoint for status events.
            lang (str, optional): Interface language ('km', 'en', 'zh'). Defaults to 'km'.
            ttl (int, optional): Session timeout in minutes (1 to 1440). Defaults to 5.

        Returns:
            dict: The API response containing the 'checkout_url', 'session_id', and 'iframe_snippet'.
        """
        self.__check_relay_token()
        
        payload = {
            "trans_id": trans_id,
            "req_custom": {
                "lang": lang,
                "ttl": ttl
            },
            "req_khqr": {
                "account_id": account_id,
                "merchant_name": merchant_name,
                "merchant_city": merchant_city,
                "amount": amount,
                "currency": currency
            },
            "req_url": {
                "return_url": return_url,
                "webhook_url": webhook_url
            }
        }
        
        response = self.__post_request("/web_checkouts/create", payload)
        
        # Optionally enhance the error message if the domain is not whitelisted
        if response.get("responseCode") == 1:
            msg = response.get("responseMessage", "")
            if "not whitelisted" in msg or "banned" in msg:
                response["responseMessage"] = f"{msg} Please whitelist your domains via Telegram: https://t.me/bakong_relay_bot?start=relay_signup"
                
        return response

    def get_webcheckout(
        self,
        session_id: str
    ) -> dict[str, Any]:
        """
        Retrieve transaction details and status of a specific Web Checkout session.

        Args:
            session_id (str): The unique alphanumeric web session identifier 
                              generated during the `create_webcheckout` process.

        Returns:
            dict: The API response containing the checkout status ('UNPAID', 'PAID', or 'EXPIRED')
                  and comprehensive transaction data if successfully paid.
        """
        self.__check_relay_token()
        
        payload = {
            "session_id": session_id
        }
        
        return self.__post_request("/web_checkouts/details", payload)