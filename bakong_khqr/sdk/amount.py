from .emv import EMV

emv = EMV()

class Amount:
    def __init__(self):
        self.__transaction_amount = emv.transaction_amount  # "54"
        self.__max_length = emv.invalid_length_amount
        
    def value(self, amount: float | int | str) -> str:
        """
        Get the formatted amount value.

        :param amount: The transaction amount to be formatted.
        :return: Formatted string including transaction amount tag, length, and amount.
        """
        if not isinstance(amount, (int, float, str)):
            raise ValueError("Amount must be a number or numeric string")

        try:
            amount_float = float(amount)
        except ValueError:
            raise ValueError(f"Invalid amount value: {amount}. Amount must be a number or a string representing a number.")

        # Format amount (no trailing zeros)
        amount_str = f"{amount_float:.2f}".rstrip("0").rstrip(".")

        # EMV length = length of VALUE ONLY
        length_of_amount = len(amount_str)

        if length_of_amount > self.__max_length:
            raise ValueError(
                f"Formatted Amount exceeds maximum length of {self.__max_length} characters."
                f"Your input length: {length_of_amount} characters."
            )

        length_str = str(length_of_amount).zfill(2)

        return f"{self.__transaction_amount}{length_str}{amount_str}"