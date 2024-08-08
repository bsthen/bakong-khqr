from .emv import EMV

# Initialize EMV instance
emv = EMV()

class MerchantName:
    def __init__(self):
        """
        Initialize the MerchantName class with settings from the EMV configuration.
        """
        self.merchant_name_tag = emv.merchant_name
        self.max_length = 25  # Maximum length for the merchant name

    def value(self, merchant_name: str) -> str:
        """
        Construct and retrieve the merchant name value with its length.

        Args:
        - merchant_name (str): The name of the merchant.

        Returns:
        - str: The constructed merchant name value with its length.
        """
        # Validate the merchant name
        if not merchant_name:
            raise ValueError("Merchant Name cannot be empty.")
        
        # Ensure the merchant name does not exceed the maximum length
        length_of_merchant_name = len(merchant_name)
        
        if length_of_merchant_name > self.max_length:
            raise ValueError(f"Merchant Name cannot exceed {self.max_length} characters. Your input length: {length_of_merchant_name} characters.")
        
        # Calculate the length of the merchant name
        length = length_of_merchant_name
        length_str = f'{length:02}'

        # Construct the result string
        result = f'{self.merchant_name_tag}{length_str}{merchant_name}'
        return result
