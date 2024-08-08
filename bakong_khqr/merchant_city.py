from .emv import EMV

# Initialize EMV instance
emv = EMV()

class MerchantCity:
    def __init__(self):
        """
        Initialize the MerchantCity class with settings from the EMV configuration.
        """
        self.merchant_city_tag = emv.merchant_city

    def value(self, merchant_city: str) -> str:
        """
        Construct and retrieve the merchant city value with its length.

        Args:
        - merchant_city (str): The name of the merchant's city.

        Returns:
        - str: The constructed merchant city value with its length.
        """
        # Validate the merchant city
        if not merchant_city:
            raise ValueError("Merchant city cannot be empty.")
        
        # Calculate the length of the merchant city
        length = len(merchant_city)
        length_str = f'{length:02}'

        # Construct the result string
        result = f'{self.merchant_city_tag}{length_str}{merchant_city}'
        return result
