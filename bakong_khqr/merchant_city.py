from .emv import EMV

# Initialize EMV instance
emv = EMV()

class MerchantCity:
    def __init__(self):
        """
        Initialize the MerchantCity class with settings from the EMV configuration.
        """
        self.merchant_city_tag = emv.merchant_city
        self.max_length = emv.invalid_length_merchant_city

    def value(self, merchant_city: str) -> str:
        """
        Construct and retrieve the merchant city value with its length.

        Args:
        - merchant_city (str): The name of the merchant's city.

        Returns:
        - str: The constructed merchant city value with its length.

        Raises:
        - ValueError: If `merchant_city` is empty or exceeds the maximum allowed length.
        """
        # Validate the merchant city
        if not merchant_city:
            raise ValueError("Merchant city cannot be empty.")
        
        # Ensure the merchant city does not exceed the maximum allowed length
        length_of_merchant_city = len(merchant_city)
        
        if length_of_merchant_city > self.max_length:
            raise ValueError(f"Merchant City cannot exceed {self.max_length} characters. Your input length: {length_of_merchant_city} characters.")
        
        # Calculate the length of the merchant city
        length_str = f'{length_of_merchant_city:02}'

        # Construct the result string
        result = f'{self.merchant_city_tag}{length_str}{merchant_city}'
        return result
