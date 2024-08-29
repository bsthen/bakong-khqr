from .emv import EMV

# Initialize EMV instance
emv = EMV()

class PayloadFormatIndicator:
    def __init__(self):
        """
        Initialize the PayloadFormatIndicator class with settings from the EMV configuration.
        """
        self.payload_format_indicator = emv.payload_format_indicator
        self.default_payload_format_indicator = emv.default_payload_format_indicator

    def value(self) -> str:
        """
        Construct and retrieve the payload format indicator value.

        Returns:
        - str: The constructed payload format indicator value.
        """
        # Calculate the length of the default payload format indicator
        length = len(self.default_payload_format_indicator)
        length_str = f'{length:02}'

        # Construct the result string
        return f'{self.payload_format_indicator}{length_str}{self.default_payload_format_indicator}'
