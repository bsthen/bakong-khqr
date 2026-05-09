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

            # Handle specific status codes
            if response.status == 200:
                try:
                    data = json.loads(response_data)
                    if not isinstance(data, dict):
                        raise ValueError("API returned valid JSON but it is not a dictionary.")
                    return data
                except json.JSONDecodeError:
                    raise ValueError(f"Bakong returned invalid JSON: {response_data}")
            
            # Mapping statuses to messages
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
        bank_account: str,
        merchant_name: str,
        merchant_city: str,
        amount: float,
        currency: str,
        store_label: str | None = None,
        phone_number: str | None = None,
        bill_number: str | None = None,
        terminal_label: str | None = None,
        static: bool = False,
        expiration: int = 1
    ) -> str:
        """
        Create a KHQR string compliant with the Bakong system.

        Args:
            bank_account (str): Bank account ID from Bakong (e.g., 'your_name@bank').
            merchant_name (str): Name of the merchant (e.g., 'Your Name').
            merchant_city (str): City of the merchant (e.g., 'Phnom Penh').
            amount (float | int): Transaction amount.
            currency (str): Currency code, either 'USD' or 'KHR'.
            store_label (str, optional): Store label or ID.
            phone_number (str, optional): Merchant's mobile number (e.g., '85512345678').
            bill_number (str, optional): Unique bill or transaction reference.
            terminal_label (str, optional): Terminal ID or a short description.
            static (bool): Set to **True** for a static QR (no amount); Defaults to **False** (Dynamic).
            expiration (int): Expiration time in days. Defaults to 1 day.

        Returns:
            str: A formatted EMVCo-compliant KHQR string.
        """
        
        if amount <= 0:
            static = True
        
        qr_data = self.__payload_format_indicator.value()
        qr_data += self.__point_of_initiation.static() if static else self.__point_of_initiation.dynamic()
        qr_data += self.__global_unique_identifier.value(bank_account)
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
        md5: str
        ) -> str:
        """
        Check the payment status of a transaction by its MD5 hash.

        Args:
            md5 (str): The MD5 hash of the QR code generated via `generate_md5()`.
            
        Returns:
            str: The transaction status. Common values are `PAID` or `UNPAID`.
        
        Note:
            A status of **UNPAID** may indicate that the transaction is still pending 
            or that the QR code has not been scanned yet.
        """
        
        payload = {
            "md5": md5
        }
        
        response = self.__post_request("/check_transaction_by_md5", payload)
        
        if response.get("responseCode") == 0:
            return "PAID"
        
        return "UNPAID"
    
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