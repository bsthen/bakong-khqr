from .emv import EMV

# Initialize EMV instance
emv = EMV()

class PointOfInitiation:
    def __init__(self):
        """
        Initialize the PointOfInitiation class with dynamic and static QR code settings from the EMV configuration.
        """
        self.__dynamic_qr = emv.default_dynamic_qr
        self.__static_qr = emv.default_static_qr

    def dynamic(self) -> str:
        """
        Retrieve the dynamic QR code setting.

        Returns:
        - str: The dynamic QR code setting.
        """
        return self.__dynamic_qr
    
    def static(self) -> str:
        """
        Retrieve the static QR code setting.

        Returns:
        - str: The static QR code setting.
        """
        return self.__static_qr
