from .emv import EMV
import time

# Initialize EMV instance
emv = EMV()

class TimeStamp:
    def __init__(self):
        """
        Initialize the TimeStamp class with parameters from the EMV configuration.
        """
        self.language_preference = emv.language_perference
        self.timestamp_tag = emv.timestamp_tag

    def value(self) -> str:
        """
        Generate the QR code data for the current timestamp.

        Returns:
        - str: Formatted QR code data including language preference, timestamp, and related tags.
        """
        # Get the current timestamp in milliseconds
        timestamp = str(int(time.time() * 1000))

        # Format the length of the timestamp
        length_of_timestamp = str(len(timestamp)).zfill(2)

        # Create the initial result with language preference and timestamp
        result = f"{self.language_preference}{length_of_timestamp}{timestamp}"

        # Format the length of the result
        length_result = str(len(result)).zfill(2)

        # Append the timestamp tag and formatted result
        result = f"{self.timestamp_tag}{length_result}{result}"

        return result
