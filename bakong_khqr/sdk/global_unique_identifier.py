from .emv import EMV

emv = EMV()

class GlobalUniqueIdentifier:
    def __init__(self):
        """
        Initialize the GlobalUniqueIdentifier class with settings from the EMV configuration.
        """
        self.__payload_format_indicator = emv.payload_format_indicator
        self.__merchant_account_information_individual = emv.merchant_account_information_individual
        self.__max_length = emv.invalid_length_bakong_account

    def value(self, account_id: str) -> str:
        """
        Generate the global unique identifier based on the account ID.

        Args:
        - account_id (str): The account ID.

        Returns:
        - str: The formatted global unique identifier.

        Raises:
        - TypeError: If `account_id` is not a string.
        - ValueError: If `account_id` exceeds the maximum allowed length.
        """
        if not isinstance(account_id, str):
            raise TypeError("Account ID must be a string.")
        
        # Ensure the account ID does not exceed the maximum allowed length
        length_of_account_id = len(account_id)
        
        if length_of_account_id > self.__max_length:
            raise ValueError(f"Account ID cannot exceed {self.__max_length} characters. Your input length: {length_of_account_id} characters.")
        
        # Calculate the length of the account ID
        length_of_account_id = f"{length_of_account_id:02}"
        
        # Generate the result string
        result = f"{self.__payload_format_indicator}{length_of_account_id}{account_id}"
        
        # Calculate the length of the result
        length_result = f"{len(result):02}"
        
        # Final result
        return f"{self.__merchant_account_information_individual}{length_result}{result}"
