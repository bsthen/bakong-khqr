from .emv import EMV

# Initialize EMV instance
emv = EMV()

class TransactionCurrency:
    def __init__(self):
        # Define currency codes based on EMV configuration
        self.transaction_currency = emv.transaction_currency
        self.currency_usd = emv.transaction_currency_usd
        self.currency_khr = emv.transaction_currency_khr

    def value(self, currency: str) -> str:
        """
        Generate the QR code data for the transaction currency.

        Parameters:
        - currency (str): Currency code, either 'USD' or 'KHR'.

        Returns:
        - str: Formatted QR code data for the specified currency.

        Raises:
        - ValueError: If the currency code is not 'USD' or 'KHR'.
        """
        currency = currency.upper()  # Normalize currency input

        if currency == "USD":
            currency_value = self.currency_usd
            
        elif currency == "KHR":
            currency_value = self.currency_khr
            
        else:
            raise ValueError(f"Invalid currency code '{currency}'. Supported codes are 'USD' and 'KHR'.")

        # Format the length of the currency value
        length_of_currency = str(len(currency_value)).zfill(2)
        return f"{self.transaction_currency}{length_of_currency}{currency_value}"
