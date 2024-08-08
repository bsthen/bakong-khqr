# bakong-khqr

SDK for creating QR codes for transactions supported by the Bakong app.

## Installation

```bash
pip install bakong-khqr
```

## Usage

The bakong-khqr package provides the KHQR class for generating QR code data for Bakong transactions.

### Importing the Library

You can import the KHQR class from the package as follows:

```bash
from bakong_khqr import KHQR
```

### Creating QR Code Data

To generate QR code data for a transaction, create an instance of the KHQR class and call the create_qr method with the required parameters.

Example:

```bash
from bakong_khqr import KHQR

# Create an instance of KHQR
khqr = KHQR()

# Generate QR code data for a transaction
qr_data = khqr.create_qr(
    bank_account='sothen_ban@wing',
    merchant_name='Sothen Ban',
    merchant_city='Phnom Penh',
    amount='1.00',
    currency='USD',
    store_label='Sothen Shop',
    phone_number='855963322209',
    bill_number='TRX019283775',
    terminal_label='Buy Course'
)

# Print or use the generated QR code data
print(qr_data)
```

### Parameters for `create_qr` Method

- `bank_account`: The bank account associated with the transaction.
- `merchant_name`: Name of the merchant.
- `merchant_city`: City where the merchant is located.
- `amount`: Amount to be transacted.
- `currency`: Currency of the transaction (e.g., 'USD', 'KHR').
- `store_label`: Label or name of the store.
- `phone_number`: Contact phone number.
- `bill_number`: Reference number for the bill.
- `terminal_label`: Label for the terminal.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## Contact

For any questions or feedback, you can contact [ME](mailto:bansokthen@gmail.com).
