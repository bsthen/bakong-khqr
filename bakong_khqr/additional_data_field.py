from .emv import EMV

emv = EMV()

class AdditionalDataField:
    def __init__(self):
        self.additional_data_tag = emv.addtion_data_tag
        self.store_label_tag = emv.store_label
        self.mobile_number_tag = emv.addition_data_field_mobile_number
        self.bill_number_tag = emv.billnumber_tag
        self.terminal_label_tag = emv.terminal_label

    def _format_value(self, tag, value) -> str:
        """
        Helper method to format a tag-value pair with length prefix.

        :param tag: The tag associated with the value.
        :param value: The value to be formatted.
        :return: Formatted tag-value string with length prefix.
        """
        value_str = str(value)
        length_of_value = f'{len(value_str):02}'
        return f'{tag}{length_of_value}{value_str}'

    def store_label_value(self, store_label) -> str:
        return self._format_value(self.store_label_tag, store_label)
    
    def phone_number_value(self, phone_number) -> str:
        return self._format_value(self.mobile_number_tag, phone_number)
    
    def bill_number_value(self, bill_number) -> str:
        return self._format_value(self.bill_number_tag, bill_number)
    
    def terminal_label_value(self, terminal_label) -> str:
        return self._format_value(self.terminal_label_tag, terminal_label)
    
    def value(self, store_label, phone_number, bill_number, terminal_label) -> str:
        """
        Combine all formatted values into a single string with a length prefix.

        :param store_label: The store label.
        :param phone_number: The phone number.
        :param bill_number: The bill number.
        :param terminal_label: The terminal label.
        :return: Combined formatted string with length prefix.
        """
        combined_data = (
            self.bill_number_value(bill_number) +
            self.phone_number_value(phone_number) +
            self.store_label_value(store_label) +
            self.terminal_label_value(terminal_label)
        )
        length_of_combined_data = f'{len(combined_data):02}'
        return f'{self.additional_data_tag}{length_of_combined_data}{combined_data}'
