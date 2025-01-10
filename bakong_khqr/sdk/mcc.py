from .emv import EMV

# Initialize EMV instance
emv = EMV()

class MCC:
    def __init__(self):
        """
        Initialize the MCC class with settings from the EMV configuration.
        """
        self.__merchant_category_code_tag = emv.merchant_category_code
        self.__default_merchant_category_code = emv.default_merchant_category_code

    def value(self, category_code: str = None) -> str:
        """
        Construct and retrieve the merchant category code value with its length.

        Args:
        - category_code (str, optional): The merchant category code. If not provided, uses the default value.

        Returns:
        - str: The constructed merchant category code value with its length.
        """
        # Use the default category code if none is provided
        if not category_code:
            category_code = self.__default_merchant_category_code
        
        # Validate the category code
        if not category_code.isdigit() or len(category_code) < 4:
            raise ValueError("Category code must be a numeric string with at least 4 digits.")

        # Calculate the length of the category code
        length_str = f'{len(category_code):02}'

        # Construct the result string
        return f'{self.__merchant_category_code_tag}{length_str}{category_code}'
