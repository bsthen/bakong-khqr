from .emv import EMV

emv = EMV()

class CRC:
    def __init__(self):
        self.__crc = emv.crc
        self.__default_crc_tag = emv.default_crc_tag
        
    def __calculate_crc16(self, data: str) -> int:
        """
        Calculate CRC-16 using the CRC-CCITT polynomial.
        
        :param data: Input data as a string
        :return: Computed CRC-16 value
        """
        crc = 0xFFFF  # Initial CRC value
        polynomial = 0x1021  # CRC-CCITT polynomial

        for byte in data.encode('utf-8'):
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1
                crc &= 0xFFFF  # Ensure it stays 16-bit
        return crc

    def __crc16_hex(self, data: str) -> str:
        """
        Get the CRC-16 value in hexadecimal format.
        
        :param data: Input data as a string
        :return: CRC-16 value as a hexadecimal string
        """
        crc16_result = self.__calculate_crc16(data)
        return format(crc16_result, '04X')
    
    def value(self, data: str) -> str:
        """
        Compute the CRC-16 value including the CRC tag and format it.
        
        :param data: Input data as a string
        :return: Formatted string including CRC tag and CRC value
        """
        crc16_hex = self.__crc16_hex(data + self.__default_crc_tag)
        length_of_crc = f'{len(crc16_hex):02}'
        return f'{self.__crc}{length_of_crc}{crc16_hex}'