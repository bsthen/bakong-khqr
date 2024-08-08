from .payload_format_indicator import PayloadFormatIndicator
from .point_of_initiation import PointOfInitiation
from .additional_data_field import AdditionalDataField
from .amount import Amount
from .country_code import CountryCode
from .crc import CRC
from .global_unique_identifier import GlobalUniqueIdentifier
from .hash import HASH
from .mcc import MCC
from .merchant_city import MerchantCity
from .merchant_name import MerchantName
from .timestamp import TimeStamp
from .transaction_currency import TransactionCurrency

class KHQR:
    def __init__(self):
        self.payload_format_indicator = PayloadFormatIndicator()
        self.point_of_initiation = PointOfInitiation()
        self.additional_data_field = AdditionalDataField()
        self.amount = Amount()
        self.country_code = CountryCode()
        self.crc = CRC()
        self.global_unique_identifier = GlobalUniqueIdentifier()
        self.hash = HASH()
        self.mcc = MCC()
        self.merchant_city = MerchantCity()
        self.merchant_name = MerchantName()
        self.timestamp = TimeStamp()
        self.transaction_currency = TransactionCurrency()
    
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
