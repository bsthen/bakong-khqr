# bakong-khqr (Unofficial)

A Python library for generating QR codes transactions compliant with the Bakong KHQR standard.

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
    amount=1.00,
    currency='USD',
    store_label='Shop A',
    phone_number='85512345678',
    bill_number='TRX019283775',
    terminal_label='Buy Course'
)

# Print or use the generated QR code data
print(qr_data)
# Result: 00020101021229190015sothen_ban@wing520459995802KH5910Sothen Ban6010Phnom Penh99170013172309296559054011530384062550112TRX0192837750211855156052270306Shop A0710Buy Course63040D95
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

## Bakong Official Documentation

KHQR SDK Documentation: [https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20SDK%20Document.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20SDK%20Document.pdf)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/bsthen/bakong-khqr/blob/main/LICENSE) file for details.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## Contact

For any questions or feedback, you can contact [ME](mailto:bansokthen@gmail.com).
