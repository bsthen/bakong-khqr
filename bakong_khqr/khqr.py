import requests

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
    def __init__(self, bakong_token: str):
        self.crc = CRC()
        self.mcc = MCC()
        self.hash = HASH()
        self.amount = Amount()
        self.timestamp = TimeStamp()
        self.country_code = CountryCode()
        self.merchant_city = MerchantCity()
        self.merchant_name = MerchantName()
        self.point_of_initiation = PointOfInitiation()
        self.transaction_currency = TransactionCurrency()
        self.additional_data_field = AdditionalDataField()
        self.payload_format_indicator = PayloadFormatIndicator()
        self.global_unique_identifier = GlobalUniqueIdentifier()
        self.bakong_token = bakong_token
        self.bakong_api = "https://api-bakong.nbc.gov.kh/v1"
    
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
        terminal_label: str
    ) -> str:
        """
        Create a QR code string based on provided information.

        :param bank_account: Bank account information.
        :param merchant_name: Name of the merchant.
        :param merchant_city: City of the merchant.
        :param amount: Transaction amount.
        :param currency: Currency code.
        :param store_label: Store label.
        :param phone_number: Mobile number.
        :param bill_number: Bill number.
        :param terminal_label: Terminal label.
        :return: Generated QR code string.
        """
        qr_data = self.payload_format_indicator.value()
        qr_data += self.point_of_initiation.dynamic()
        qr_data += self.global_unique_identifier.value(bank_account)
        qr_data += self.mcc.value()
        qr_data += self.country_code.value()
        qr_data += self.merchant_name.value(merchant_name)
        qr_data += self.merchant_city.value(merchant_city)
        qr_data += self.timestamp.value()
        qr_data += self.amount.value(amount)
        qr_data += self.transaction_currency.value(currency)
        qr_data += self.additional_data_field.value(store_label, phone_number, bill_number, terminal_label)
        qr_data += self.crc.value(qr_data)
        return qr_data

    def get_deeplink(
        self, 
        qr: str, 
        callback: str = "https://bakong.nbc.org.kh", 
        appIconUrl: str = "https://bakong.nbc.gov.kh/images/logo.svg", 
        appName: str = "MyAppName"
        ) -> str:
        """
        Generate a deep link for the QR code.

        :param qr: QR code string.
        :param callback: Callback URL for the deep link.
        :param appIconUrl: App icon URL of your app or website.
        :param appName: Name of your app or website.
        :return: Deep link URL as a string.
        """
        payload = {
            "qr": qr,
            "sourceInfo": {
                "appIconUrl": appIconUrl,
                "appName": appName,
                "appDeepLinkCallback": callback
            }
        }
        headers = {
            "Authorization": f"Bearer {self.bakong_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.bakong_api + "/generate_deeplink_by_qr", json=payload, headers=headers).json()
        
        if response["responseCode"] == 0:
            return response["data"]["shortLink"]
        
        if response["responseCode"] == 1:
            raise ValueError("Error: ", response["status"]["message"])
        
    def get_md5(
        self, 
        qr: str
        ) -> str:
        """
        Generate an MD5 hash for the QR code.

        :param qr: QR code string.
        :return: MD5 hash as a string.
        """
        return self.hash.md5(qr)
    
    def is_paid(
        self, 
        md5: str
        ) -> bool:
        """
        Check the transaction status based on the MD5 hash.

        :param md5: MD5 hash of the QR code.
        :return: True (paid) or False (unpaid).
        """
        payload = {
            "md5": md5
        }
        headers = {
            "Authorization": f"Bearer {self.bakong_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.bakong_api + "/check_transaction_by_md5", json=payload, headers=headers).json()
        
        if response["responseCode"] == 0:
            return True
        return False