from .emv import EMV
import time

# Initialize EMV instance
emv = EMV()

class TimeStamp:
    def __init__(self):
        """
        Initialize the TimeStamp class with parameters from the EMV configuration.
        """
        self.__language_preference = emv.language_perference
        self.__language_preference_exp = emv.language_perference_exp
        self.__timestamp_tag = emv.timestamp_tag

    def value(self, exp: int = 1) -> str:
        """
        Generate the QR code data for the current timestamp.
        Parameters:
        - exp (int): Expiration time in seconds (default: 1 Day or 24 hours). This is used to calculate the expiration time for the QR code.

        Returns:
        - str: Formatted QR code data including language preference, timestamp, and related tags.
        """
        
        # check if exp is less than 1 day (24 hours)
        if exp < 1:
            raise ValueError("Expiration time cannot be less than 1 day. Your input: {exp} days.")
        
        # Convert expiration time from days to seconds
        exp = exp * 86400
        
        # Get the current timestamp in milliseconds
        timestamp = str(int(time.time() * 1000))
        
        expiration_time = str(int(time.time() * 1000) + exp)

        # Format the length of the timestamp
        length_of_timestamp = str(len(timestamp)).zfill(2)
        
        # Format the length of the expiration time
        length_of_expiration_time = str(len(expiration_time)).zfill(2)

        # Create the initial result with language preference and timestamp
        result = f"{self.__language_preference}{length_of_timestamp}{timestamp}"
        # Append the expiration time to the result
        result += f"{self.__language_preference_exp}{length_of_expiration_time}{expiration_time}"

        # Format the length of the result
        length_result = str(len(result)).zfill(2)

        # Append the timestamp tag and formatted result
        return f"{self.__timestamp_tag}{length_result}{result}"
