import hashlib

class HASH:
    def __init__(self):
        """
        Initialize the HASH class.
        """
        pass

    def md5(self, data: str) -> str:
        """
        Generate an MD5 hash for the given data.

        Args:
        - data (str): The data to hash.

        Returns:
        - str: The hexadecimal MD5 hash of the input data.

        Raises:
        - TypeError: If `data` is not a string.
        """
        if not isinstance(data, str):
            raise TypeError("Data must be a string.")
        
        # Generate and return the MD5 hash of the input data
        return hashlib.md5(data.encode('utf-8')).hexdigest()
