from .emv import EMV

emv = EMV()

class GlobalUniqueIdentifier:
    def __init__(self):
        """
        Initialize the GlobalUniqueIdentifier class.
        """
        self.payload_format_indicator = emv.payload_format_indicator
        self.merchant_account_information_individual = emv.merchant_account_information_individual

    def value(self, bank_account: str) -> str:
        """
        Generate the global unique identifier based on the bank account.

        Args:
        - bank_account (str): The bank account number.

        Returns:
        - str: The formatted global unique identifier.

        Raises:
        - TypeError: If `bank_account` is not a string.
        """
        if not isinstance(bank_account, str):
            raise TypeError("Bank account must be a string.")
        
        # Ensure the length of the bank account number
        length_of_bank_account = f"{len(bank_account):02}"
        
        # Generate the result string
        result = f"{self.payload_format_indicator}{length_of_bank_account}{bank_account}"
        
        # Ensure the length of the result
        length_result = f"{len(result):02}"
        
        result = f"{self.merchant_account_information_individual}{length_result}{result}"
        return result
