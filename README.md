# bakong-khqr (Unofficial)

A Python library for generating QR codes transactions compliant with the Bakong KHQR standard.

## Requirement

- Python3
- Bakong Developer Token [https://api-bakong.nbc.gov.kh/register](https://api-bakong.nbc.gov.kh/register)

## Installation

```bash
pip3 install bakong-khqr
```

## Usage

The bakong-khqr package provides the KHQR class for generating QR code, Deeplink, Check Transaction for Bakong KHQR.

### Importing the Library

You can import the KHQR class from the package as follows:

```bash
from bakong_khqr import KHQR
```

### Creating QR Code Data

To generate QR code data for a transaction, create an instance of the KHQR() class with Bakong Token and call the:

- create_qr() method with the required parameters.
- get_deeplink() method with the required parameters.
- get_md5() method with the required parameters.
- is_paid() method with the required parameters.

Example:

```bash
from bakong_khqr import KHQR

# Create an instance of KHQR with Bakong Developer Token
khqr = KHQR("eyJhbGciOiJIUzI1NiIsI...nMhgG87BWeDg9Lu-_CKe1SMqC0")

# Generate QR code data for a transaction
qr = khqr.create_qr(
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

# Generate Deeplink
deeplink = khqr.get_deeplink(
    qr,
    callback="https://bakong.nbc.org.kh",
    appIconUrl="https://your_website.com/images/logo.png",
    appName="MyAppName"
)

# Get Hash MD5
md5 = khqr.get_md5(qr)

# Check Transaction paid or unpaid
is_paid = khqr.is_paid(md5)


# Print or use the generated QR code data

print(qr)
# String Result: 00020101021229190015sothen_ban@wing520459995802KH5910Sothen Ban6010Phnom Penh99170013172309296559054011530384062550112TRX0192837750211855156052270306Shop A0710Buy Course63040D95

print(deeplink)
# String Result: https://bakong.page.link/jRUTZ....hsspf9

print(md5)
# String Result: 3ed4fe62ed7758785f5fc3b5f37faded

print(is_paid)
# Boolean Result: False

```

#### Parameters for `create_qr()` Method

- `bank_account`: The bank account associated with the transaction.
- `merchant_name`: Name of the merchant.
- `merchant_city`: City where the merchant is located.
- `amount`: Amount to be transacted.
- `currency`: Currency of the transaction (e.g., 'USD', 'KHR').
- `store_label`: Label or name of the store.
- `phone_number`: Contact phone number.
- `bill_number`: Reference number for the bill.
- `terminal_label`: Label for the terminal.

#### Parameters for `get_deeplink()` Method

- `qr`: Valid QR Code data as string that generate from create_qr() method.
- `callback`: Deeplink URL for opening your app after payment is completed.
- `appIconUrl`: Your App Icon URL.
- `appName`: Your App Name.

#### Parameters for `md5()` Method

- `qr`: Valid QR Code data as string that generate from create_qr() method.

#### Parameters for `is_paid()` Method

- `md5`: Valid hash md5 from md5() method of the correct transaction.

## Bakong Official

KHQR SDK Documentation: [https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20SDK%20Document.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20SDK%20Document.pdf)

Development API: [https://sit-api-bakong.nbc.gov.kh/](https://sit-api-bakong.nbc.gov.kh/)

Production API: [https://api-bakong.nbc.gov.kh/](https://api-bakong.nbc.gov.kh/)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/bsthen/bakong-khqr/blob/main/LICENSE) file for details.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## Contact

For any questions or feedback, you can contact [ME](mailto:bansokthen@gmail.com).
