from .emv import EMV

# Initialize EMV instance
emv = EMV()

class AdditionalDataField:
    def __init__(self):
        """
        Initialize the AdditionalDataField class with settings from the EMV configuration.
        """
        self.__additional_data_tag = emv.addtion_data_tag
        self.__store_label_tag = emv.store_label
        self.__mobile_number_tag = emv.addition_data_field_mobile_number
        self.__bill_number_tag = emv.billnumber_tag
        self.__terminal_label_tag = emv.terminal_label
        
        # Maximum lengths according to EMVCo / Bakong spec
        self.__store_label_max = emv.invalid_length_store_label
        self.__mobile_max = emv.invalid_length_mobile_number
        self.__bill_max = emv.invalid_length_bill_number
        self.__terminal_max = emv.invalid_length_terminal_label

    def __format_field(self, tag: str, value: str) -> str:
        """Format a single sub-field: TAG + LENGTH (02) + VALUE"""
        value_str = str(value).strip()
        if not value_str:
            return ""
        length = f"{len(value_str):02d}"
        return f"{tag}{length}{value_str}"

    def __validate_length(self, value: str, max_length: int, field_name: str):
        """
        Validate the length of a field value.

        :param value: The value to be validated.
        :param field_name: The name of the field for error reporting.
        :raises ValueError: If the value exceeds the maximum allowed length.
        """
        if len(value) > max_length:
            raise ValueError(f"{field_name} cannot exceed {max_length} characters. Your input length: {len(value)} characters.")
    
    def value(
        self,
        store_label: str | None = None,
        phone_number: str | None = None,
        bill_number: str | None = None,
        terminal_label: str | None = None,
        ) -> str:
        """
        Combine all formatted values into a single string with a length prefix.

        :param store_label: The store label.
        :param phone_number: The phone number.
        :param bill_number: The bill number.
        :param terminal_label: The terminal label.
        :return: Combined formatted string with length prefix.
        """
        sub_fields = []

        # Store Label (usually Tag 03)
        if store_label:
            self.__validate_length(store_label, self.__store_label_max, "Store label")
            sub_fields.append(self.__format_field(self.__store_label_tag, store_label))

        # Phone Number (usually Tag 04) - with Khmer phone normalization
        if phone_number:
            digits = ''.join(c for c in str(phone_number) if c.isdigit())
            if digits.startswith('855'):
                digits = digits[3:]
            if not digits.startswith('0'):
                digits = '0' + digits

            self.__validate_length(digits, self.__mobile_max, "Phone number")
            sub_fields.append(self.__format_field(self.__mobile_number_tag, digits))

        # Bill Number (usually Tag 05)
        if bill_number:
            self.__validate_length(bill_number, self.__bill_max, "Bill number")
            sub_fields.append(self.__format_field(self.__bill_number_tag, bill_number))

        # Terminal Label (usually Tag 07)
        if terminal_label:
            self.__validate_length(terminal_label, self.__terminal_max, "Terminal label")
            sub_fields.append(self.__format_field(self.__terminal_label_tag, terminal_label))

        if not sub_fields:
            # No additional data → return empty (do not include tag 62 at all)
            return ""

        combined = "".join(sub_fields)
        total_length = f"{len(combined):02d}"

        # Final format: 62 + LL + subfields
        return f"{self.__additional_data_tag}{total_length}{combined}"
