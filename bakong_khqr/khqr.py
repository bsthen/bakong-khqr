import requests
from typing import Optional

from .sdk.crc import CRC
from .sdk.mcc import MCC
from .sdk.hash import HASH
from .sdk.amount import Amount
from .sdk.timestamp import TimeStamp
from .sdk.country_code import CountryCode
from .sdk.merchant_city import MerchantCity
from .sdk.merchant_name import MerchantName
from .sdk.point_of_initiation import PointOfInitiation
from .sdk.transaction_currency import TransactionCurrency
from .sdk.additional_data_field import AdditionalDataField
from .sdk.payload_format_indicator import PayloadFormatIndicator
from .sdk.global_unique_identifier import GlobalUniqueIdentifier

class KHQR:
    def __init__(self, bakong_token: str = None):
        self.__crc = CRC()
        self.__mcc = MCC()
        self.__hash = HASH()
        self.__amount = Amount()
        self.__timestamp = TimeStamp()
        self.__country_code = CountryCode()
        self.__merchant_city = MerchantCity()
        self.__merchant_name = MerchantName()
        self.__point_of_initiation = PointOfInitiation()
        self.__transaction_currency = TransactionCurrency()
        self.__additional_data_field = AdditionalDataField()
        self.__payload_format_indicator = PayloadFormatIndicator()
        self.__global_unique_identifier = GlobalUniqueIdentifier()
        self.__bakong_token = bakong_token
        self.__bakong_api = "https://api-bakong.nbc.gov.kh/v1"
        
    def __check_bakong_token(self):
        if not self.__bakong_token:
            raise ValueError("Bakong Developer Token is required for KHQR class initialization. Example usage: khqr = KHQR('your_token_here').")

    
    def create_qr(
        self,
        bank_account: str,
        merchant_name: str,
        merchant_city: str,
        amount: float,
        currency: str,
        store_label: str,
        phone_number: str,
        bill_number: str,
        terminal_label: str,
        static: Optional[bool] = False,
    ) -> str:
        """
        Create a QR code string based on provided information.

        :param bank_account: Bank account information from Bakong profile (e.g., your_name@aba).
        :param merchant_name: Name of the merchant (e.g., Your Name).
        :param merchant_city: City of the merchant (e.g., Phnom Penh).
        :param amount: Transaction amount (e.g., 1.09).
        :param currency: Currency code (e.g., USD or KHR).
        :param store_label: Store label or merchant reference (e.g., Shop A).
        :param phone_number: Mobile number of the merchant (e.g., 85512345678).
        :param bill_number: Bill number or transaction reference (e.g., TRX019283775).
        :param terminal_label: Terminal label or transaction description (e.g., Buy Course).
        :param static: Static or Dynamic QR code (default: False).
        :return: Generated QR code as a string.
        """
        qr_data = self.__payload_format_indicator.value()
        qr_data += self.__point_of_initiation.static() if static else self.__point_of_initiation.dynamic()
        qr_data += self.__global_unique_identifier.value(bank_account)
        qr_data += self.__mcc.value()
        qr_data += self.__country_code.value()
        qr_data += self.__merchant_name.value(merchant_name)
        qr_data += self.__merchant_city.value(merchant_city)
        qr_data += self.__timestamp.value()
        if not static:
            qr_data += self.__amount.value(amount)
        qr_data += self.__transaction_currency.value(currency)
        qr_data += self.__additional_data_field.value(store_label, phone_number, bill_number, terminal_label)
        qr_data += self.__crc.value(qr_data)
        return qr_data

    def generate_deeplink(
        self, 
        qr: str, 
        callback: str = "https://bakong.nbc.org.kh", 
        appIconUrl: str = "https://bakong.nbc.gov.kh/images/logo.svg", 
        appName: str = "MyAppName"
        ) -> str:
        """
        Generate a deep link for the QR code.

        :param qr: QR code string generated from create_qr() method.
        :param callback: Callback URL for the deep link (default: https://bakong.nbc.org.kh).
        :param appIconUrl: App icon URL of your app or website (default: https://bakong.nbc.gov.kh/images/logo.svg).
        :param appName: Name of your app or website (default: MyAppName).
        :return: Deep link URL as a string.
        """

        self.__check_bakong_token() # Check if Bakong Developer Token is provided
        
        payload = {
            "qr": qr,
            "sourceInfo": {
                "appIconUrl": appIconUrl,
                "appName": appName,
                "appDeepLinkCallback": callback
            }
        }
        headers = {
            "Authorization": f"Bearer {self.__bakong_token}",
            "Content-Type": "application/json"
        }
        
        try:
        
            response = requests.post(self.__bakong_api + "/generate_deeplink_by_qr", json=payload, headers=headers).json()
            
            if response["responseCode"] == 0:
                return response["data"]["shortLink"]
            
            if response["responseCode"] == 1:
                raise ValueError("Error: ", response["status"]["message"])
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"An error occurred: {e}")
        
    def generate_md5(
        self, 
        qr: str
        ) -> str:
        """
        Generate an MD5 hash for the QR code.

        :param qr: QR code string generated from create_qr() method.
        :return: MD5 hash as a string (32 characters).
        """
        return self.__hash.md5(qr)
    
    def check_payment(
        self, 
        md5: str
        ) -> str:
        """
        Check the transaction status based on the MD5 hash.

        :param md5: MD5 hash of the QR code generated from generate_md5() method.
        :return: Transaction status as a string (PAID or UNPAID).
        """
        
        self.__check_bakong_token() # Check if Bakong Developer Token is provided
        
        payload = {
            "md5": md5
        }
        headers = {
            "Authorization": f"Bearer {self.__bakong_token}",
            "Content-Type": "application/json"
        }
        
        try:
        
            response = requests.post(self.__bakong_api + "/check_transaction_by_md5", json=payload, headers=headers).json()
            
            if response["responseCode"] == 0:
                return "PAID"
            
            if response["responseCode"] == 1 and response["errorCode"] == 6:
                raise ValueError("Your Developer Token is either incorrect or expired. Please renew it through Bakong Developer.",)
            
            return "UNPAID"

        except requests.exceptions.RequestException as e:
            raise ValueError(f"An error occurred: {e}")
    
    def check_bulk_payments(
        self,
        md5_list: list[str]
        ) -> list[str]:
        """
        Check the transaction status based on the list of MD5 hashes.

        :param md5_list: List of MD5 hashes generated from generate_md5() method.
        :return: md5 list of paid transactions.
        """
        
        self.__check_bakong_token()
        
        headers = {
            "Authorization": f"Bearer {self.__bakong_token}",
            "Content-Type": "application/json"
        }
        
        try:
        
            response = requests.post(self.__bakong_api + "/check_transaction_by_md5_list", json=md5_list, headers=headers).json()
            
            if response["responseCode"] == 0:
                # if md5 is SUCCESS, then append md5 to paid_list
                paid_list = []
                for data in response["data"]:
                    if data["status"] == "SUCCESS":
                        paid_list.append(data["md5"])
                return paid_list
            
            if response["responseCode"] == 1 and response["errorCode"] == 6:
                raise ValueError("Your Developer Token is either incorrect or expired. Please renew it through Bakong Developer.")
            
            return []
        
        except requests.exceptions.RequestException as e:
            raise ValueError(f"An error occurred: {e}")