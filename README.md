# bakong-khqr (Unofficial)

A Python library for generating payment transactions compliant with the Bakong KHQR standard.

## Requirement

- Python3
- Bakong Developer Token [https://api-bakong.nbc.gov.kh/register](https://api-bakong.nbc.gov.kh/register)

## Installation

```bash
pip3 install bakong-khqr
```

## Usage

The bakong-khqr package provides the KHQR class for generating QR code, Deeplink, Check Payment transaction for Bakong KHQR.

### Importing the Library

You can import the KHQR class from the package as follows:

```bash
from bakong_khqr import KHQR
```

### Creating Payment Transaction

To generate QR code data for a transaction, create an instance of the KHQR() class with Bakong Token and call the:

- create_qr() method with the required parameters.
- generate_deeplink() method with the required parameters.
- generate_md5() method with the required parameters.
- check_payment() method with the required parameters.
- check_bulk_payments() method with the required parameters.

Example:

```bash
from bakong_khqr import KHQR

# Create an instance of KHQR with Bakong Developer Token
khqr = KHQR("eyJhbGciOiJIUzI1NiIsI...nMhgG87BWeDg9Lu-_CKe1SMqC0")

# Generate QR code data for a transaction
qr = khqr.create_qr(
    bank_account='your_name@wing', # Check your address under Bakong profile (Mobile App)
    merchant_name='Your Name',
    merchant_city='Phnom Penh',
    amount=9800, #9800 Riel
    currency='KHR', # USD or KHR
    store_label='MShop',
    phone_number='85512345678',
    bill_number='TRX019283775',
    terminal_label='Buy 1A_Level_Book'
)
print(qr)
# String Result: 00020101021229180014your_name@wing520459995802KH5909Your Name6010Phnom Penh991700131724927295157541100000009800530311662610112TRX0192837750211855123456780305MShop0717Buy 1A_Level_Book63041087

# Generate Deeplink
deeplink = khqr.generate_deeplink(
    qr,
    callback="https://your_website.com/shop/details?q=ABC", # Or your app's custom scheme (e.g., mshop://purchase/39482)
    appIconUrl="https://your_website.com/images/logo.png", # Your logo image .png or .svg
    appName="MyAppName" # (e.g., MSHOP)
)
print(deeplink)
# String Result: https://bakong.page.link/CgXb....ks6az9a38

# Get Hash MD5
md5 = khqr.generate_md5(qr)
print(md5)
# String Result: dfcabf4598d1c405a75540a3d4ca099d

# Check Transaction paid or unpaid
payment_status = khqr.check_payment(md5)
print(payment_status)
# String Result: "UNPAID"
# Indicates that this transaction has not yet been paid.

# Check Bulk Transactions
md5_list = [
    "dfcabf4598d1c405a75540a3d4ca099d", 
    "5154e4f795634ff1a0ae4b48e53a6d9c",
    "a57d9bb85f52f12a20cf7beecb03d11d",
    "495fdaec0be5d94c89bc1283c7283d3d",
    "31bca02094ad576588e42b60db57bc98"
]

bulk_payments_status = khqr.check_bulk_payments(md5_list)
print(bulk_payments_status)
# List Result: ["5154e4f795634ff1a0ae4b48e53a6d9c", "495fdaec0be5d94c89bc1283c7283d3d"]
# Returns a list containing only the MD5 hashes that correspond to successful (paid) transactions.

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

#### Parameters for `generate_deeplink()` Method

- `qr`: Valid QR Code data as string that generate from create_qr() method.
- `callback`: Deeplink URL for opening your app after payment is completed.
- `appIconUrl`: Your App Icon URL.
- `appName`: Your App Name.

#### Parameters for `generate_md5()` Method

- `qr`: Valid QR Code data as string that generate from create_qr() method.

#### Parameters for `check_payment()` Method

- `md5`: Valid hash md5 from generate_md5() method of the correct transaction.

#### Parameters for `check_bulk_payments()` Method

- `md5_list`: md5 list of all transacrions generate from generate_md5() method.

## Bakong Official

KHQR SDK Documentation: [https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20SDK%20Document.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20SDK%20Document.pdf)

Development API: [https://sit-api-bakong.nbc.gov.kh/](https://sit-api-bakong.nbc.gov.kh/)

Production API: [https://api-bakong.nbc.gov.kh/](https://api-bakong.nbc.gov.kh/)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/bsthen/bakong-khqr/blob/main/LICENSE) file for details.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## Contact

For any questions or feedback, you can contact [ME](mailto:bansokthen@gmail.com) or Buy Me A Coffee ☕️ ABA: 000510062
