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

    def value(self, static: bool, expiration: int = 1) -> str:
        """
        Generate the QR code data for the current timestamp.

        Parameters:
        - static (bool): Whether the QR code is static (True) or dynamic (False).
        - expiration (int): Expiration time in days (default: 1 day). 
                            Only used when static=False.

        Returns:
        - str: Formatted QR code data including language preference, timestamp, 
               and expiration (for dynamic QR only).
        """
        
        # Get current timestamp in milliseconds
        timestamp = str(int(time.time() * 1000))
        length_of_timestamp = str(len(timestamp)).zfill(2)

        # Start building the result with language preference + timestamp
        result = f"{self.__language_preference}{length_of_timestamp}{timestamp}"

        # Only add expiration part for dynamic QR codes (static=False)
        if not static:
            if expiration < 1:
                raise ValueError(f"Expiration time cannot be less than 1 day. Your input: {expiration} days.")
            
            # Convert expiration from days to milliseconds
            exp_ms = expiration * 86400 * 1000
            expiration_time = str(int(time.time() * 1000) + exp_ms)
            length_of_expiration_time = str(len(expiration_time)).zfill(2)

            # Append expiration section
            result += f"{self.__language_preference_exp}{length_of_expiration_time}{expiration_time}"

        # Format the total length of the result
        length_result = str(len(result)).zfill(2)

        # Return final formatted string with timestamp tag
        return f"{self.__timestamp_tag}{length_result}{result}"