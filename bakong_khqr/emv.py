class EMV:
    """
    EMV Class contains constants used for encoding and decoding QR codes
    for transactions supported by the Bakong app.
    """
    
    def __init__(self):
        # Default QR Code Types
        self.default_dynamic_qr = "010212"
        self.default_static_qr = "010211"
        
        # Currency Codes
        self.transaction_currency_usd = "840"  # USD
        self.transaction_currency_khr = "116"  # KHR
        self.transaction_currency = "53"
        
        # Payload and Point of Initiation
        self.payload_format_indicator = "00"
        self.default_payload_format_indicator = "01"
        self.point_of_initiation_method = "01"  # Static (11) or Dynamic (12)
        
        # Merchant Information
        self.merchant_name = "59"
        self.merchant_city = "60"
        self.default_merchant_city = "Phnom Penh"
        self.merchant_category_code = "52"
        self.default_merchant_category_code = "5999"
        
        # QR Code Identifiers
        self.static_qr = "11"
        self.dynamic_qr = "12"
        self.merchant_account_information_individual = "29"
        self.merchant_account_information_merchant = "30"
        
        # Transaction Details
        self.transaction_amount = "54"
        self.default_transaction_amount = "0"
        self.country_code = "58"
        self.default_country_code = "KH"
        
        # Additional Data Tags
        self.addtion_data_tag = "62"
        self.billnumber_tag = "01"
        self.addition_data_field_mobile_number = "02"
        self.store_label = "03"
        self.terminal_label = "07"
        self.purpose_of_transaction = "08"
        self.timestamp_tag = "99"
        self.merchant_information_language_template = "64"
        
        # Language Preferences
        self.language_perference = "00"
        self.merchant_name_alternative_language = "01"
        self.merchant_city_alternative_language = "02"
        
        # UnionPay Specific
        self.unionpay_merchant_account = "15"
        
        # CRC Tag
        self.crc = "63"
        self.crc_length = "04"
        self.default_crc_tag = "6304"
        
        # Invalid Length Constraints
        self.invalid_length_khqr = 2
        self.invalid_length_merchant_name = 25
        self.invalid_length_bakong_account = 32
        self.invalid_length_amount = 13
        self.invalid_length_country_code = 3
        self.invalid_length_merchant_category_code = 4
        self.invalid_length_merchant_city = 15
        self.invalid_length_timestamp = 13
        self.invalid_length_transaction_amount = 14
        self.invalid_length_transaction_currency = 3
        self.invalid_length_bill_number = 25
        self.invalid_length_store_label = 25
        self.invalid_length_terminal_label = 25
        self.invalid_length_purpose_of_transaction = 25
        self.invalid_length_merchant_id = 32
        self.invalid_length_acquiring_bank = 32
        self.invalid_length_mobile_number = 25
        self.invalid_length_account_information = 32
        self.invalid_length_merchant_name_language_template = 99
        self.invalid_length_upi_merchant = 99
        self.invalid_length_language_perference = 2
        self.invalid_length_merchant_name_alternative_language = 25
        self.invalid_length_merchant_city_alternative_language = 15
