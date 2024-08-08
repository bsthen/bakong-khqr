from .emv import EMV

# Initialize EMV instance
emv = EMV()

class MerchantName:
    def __init__(self):
        """
        Initialize the MerchantName class with settings from the EMV configuration.
        """
        self.merchant_name_tag = emv.merchant_name

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
            raise ValueError("Merchant name cannot be empty.")
        
        # Calculate the length of the merchant name
        length = len(merchant_name)
        length_str = f'{length:02}'

        # Construct the result string
        result = f'{self.merchant_name_tag}{length_str}{merchant_name}'
        return result
