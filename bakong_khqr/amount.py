from .emv import EMV

emv = EMV()

class Amount:
    def __init__(self):
        self.transaction_amount = emv.transaction_amount
        
    def value(self, amount: float) -> str:
        """
        Get the formatted amount value.

        :param amount: The transaction amount to be formatted.
        :return: Formatted string including transaction amount tag, length, and amount.
        """
        if not isinstance(amount, (int, float, str)):
            raise ValueError("Amount must be a number or a string")
        
        try:
            # Convert amount to float for formatting
            amount_float = float(amount)
        except ValueError:
            raise ValueError(f"Invalid amount value: {amount}")
        
        # Format amount as a decimal with two places
        amount_str = f'{amount_float:.2f}'
        
        # Ensure amount_str has no extra decimal places
        amount_str = amount_str.rstrip('0').rstrip('.') if '.' in amount_str else amount_str
        
        # Calculate length of the formatted amount string
        length_of_amount = '0' + str(len(amount_str)) if len(amount_str) < 10 else str(len(amount_str))
        
        result = str(self.transaction_amount) + length_of_amount + amount_str
        return result
