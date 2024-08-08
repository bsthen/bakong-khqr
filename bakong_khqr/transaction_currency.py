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
        - str: Formatted QR code data for the specified currency, or an empty string if currency is invalid.
        """
        currency = currency.upper()  # Normalize currency input

        if currency == "USD":
            currency_value = self.currency_usd
        elif currency == "KHR":
            currency_value = self.currency_khr
        else:
            return ""  # Return an empty string for unsupported currencies

        # Format the length of the currency value
        length_of_currency = str(len(currency_value)).zfill(2)
        result = f"{self.transaction_currency}{length_of_currency}{currency_value}"
        
        return result
