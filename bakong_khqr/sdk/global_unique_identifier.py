from .emv import EMV

emv = EMV()

class GlobalUniqueIdentifier:
    def __init__(self):
        """
        Initialize the GlobalUniqueIdentifier class with settings from the EMV configuration.
        """
        self.payload_format_indicator = emv.payload_format_indicator
        self.merchant_account_information_individual = emv.merchant_account_information_individual
        self.max_length = emv.invalid_length_bakong_account

    def value(self, bank_account: str) -> str:
        """
        Generate the global unique identifier based on the bank account.

        Args:
        - bank_account (str): The bank account number.

        Returns:
        - str: The formatted global unique identifier.

        Raises:
        - TypeError: If `bank_account` is not a string.
        - ValueError: If `bank_account` exceeds the maximum allowed length.
        """
        if not isinstance(bank_account, str):
            raise TypeError("Bank account must be a string.")
        
        # Ensure the bank account does not exceed the maximum allowed length
        length_of_bank_account = len(bank_account)
        
        if length_of_bank_account > self.max_length:
            raise ValueError(f"Bank account cannot exceed {self.max_length} characters. Your input length: {length_of_bank_account} characters.")
        
        # Calculate the length of the bank account number
        length_of_bank_account = f"{length_of_bank_account:02}"
        
        # Generate the result string
        result = f"{self.payload_format_indicator}{length_of_bank_account}{bank_account}"
        
        # Calculate the length of the result
        length_result = f"{len(result):02}"
        
        # Final result
        return f"{self.merchant_account_information_individual}{length_result}{result}"
