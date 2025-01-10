from .emv import EMV

emv = EMV()

class CountryCode:
    def __init__(self):
        self.__country_code_tag = emv.country_code
        self.__default_country_code = emv.default_country_code
        
    def value(self, country_code: str = None) -> str:
        """
        Get the formatted country code value.

        :param country_code: Optional custom country code. If not provided, the default is used.
        :return: Formatted string including country code and its length.
        """
        # Use the default if no country code is provided
        if not country_code:
            country_code = self.__default_country_code
        
        # Calculate the length of the country code
        length_of_country_code = f'{len(country_code):02}'

        # Construct the result
        return f'{self.__country_code_tag}{length_of_country_code}{country_code}'
