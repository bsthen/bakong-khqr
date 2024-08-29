from .emv import EMV

emv = EMV()

class Amount:
    def __init__(self):
        self.transaction_amount = emv.transaction_amount
        self.max_length = emv.invalid_length_amount
        
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
            raise ValueError(f"Invalid amount value: {amount}. Amount must be a number or a string representing a number.")
        
        # Format amount as a decimal with two places
        amount_str = f'{amount_float:.2f}'
        
        # Ensure amount_str has no extra decimal places
        amount_str = amount_str.rstrip('0').rstrip('.') if '.' in amount_str else amount_str
        
        # Ensure length of formatted amount is always 13 characters
        length_of_amount = len(amount_str) + 2  # Adding 2 for the transaction amount tag and length of amount
        
        if length_of_amount > self.max_length:
            raise ValueError(f"Formatted Amount exceeds maximum length of {self.max_length} characters. Your input length: {length_of_amount} characters.")
        
        # Pad amount_str with leading zeros to ensure it fits the required length
        padded_amount_str = amount_str.zfill(11)  # Ensures the total length (including tag and length) is 13
        
        # Calculate length of the formatted amount string
        length_of_amount = str(len(padded_amount_str)).zfill(2)  # Length in 2 digits
        
        return f"{self.transaction_amount}{length_of_amount}{padded_amount_str}"
