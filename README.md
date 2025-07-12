<h1 align="center"> Bakong-KHQR (Unofficial) </h1>

<p align="center">
<a href="https://www.youtube.com/watch?v=qGjQZ6V393c" target="_blank" >
        <img src="https://img.youtube.com/vi/qGjQZ6V393c/0.jpg" alt="YouTube">
    </a>
</p>

<p align="center">
A Python package for generating payment transactions compliant with the Bakong KHQR standard.
</p>

<p align="center">
    <a href="https://opensource.org/licenses/MIT" target="_blank" >
        <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
    </a>
    <a href="https://pypi.org/project/bakong-khqr/" target="_blank" >
        <img src="https://img.shields.io/pypi/v/bakong-khqr?color=%2334D058&label=pypi%20package" alt="PyPI version">
    </a>
    <a href="https://pypi.org/project/bakong-khqr/" target="_blank" >
        <img src="https://img.shields.io/pypi/pyversions/bakong-khqr.svg" alt="Python Version">
    </a>
    <a href="https://pepy.tech/projects/bakong-khqr" target="_blank" >
        <img src="https://static.pepy.tech/badge/bakong-khqr" alt="Downloads">
</a>
</p>

## Download Mobile App

- Bakong App ( [App Store](https://apps.apple.com/kh/app/bakong/id1440829141) | [Play Store](https://play.google.com/store/apps/details?id=jp.co.soramitsu.bakong) )
- Bakong Tourists ( [App Store](https://apps.apple.com/kh/app/bakong-tourists/id6471774666) | [Play Store](https://play.google.com/store/apps/details?id=kh.gov.nbc.bakong.tourist) )

## Requirement

- Python3
- Bakong Account (Full KYC)
- Bakong Developer Token [https://api-bakong.nbc.gov.kh/register](https://api-bakong.nbc.gov.kh/register)

## Installation

```bash
pip3 install bakong-khqr
```

or Update Last Version

```bash
pip3 install --upgrade bakong-khqr
```

## Usage

The bakong-khqr package provides the KHQR class for generating QR code, Deeplink, Check Payment, Get Payment transaction for Bakong KHQR.

### Importing the package

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
- get_payment() method with the required parameters.
- check_bulk_payments() method with the required parameters.

Example:

```bash
from bakong_khqr import KHQR

# Create an instance of KHQR with Bakong Developer Token:
khqr = KHQR("eyJhbGciOiJIUzI1NiIsI...nMhgG87BWeDg9Lu-_CKe1SMqC0")

# Generate QR code data for a transaction:
qr = khqr.create_qr(
    bank_account='user_name@bank', # Check your user_name@bank under Bakong profile (Mobile App)
    merchant_name='Your Name',
    merchant_city='Phnom Penh',
    amount=9800, #9800 Riel
    currency='KHR', # USD or KHR
    store_label='MShop',
    phone_number='85512345678',
    bill_number='TRX01234567',
    terminal_label='Cashier-01',
    static=False # Static or Dynamic QR code (default: False)
)
print(qr)
# String Result: 00020101021229180014user_name@bank520459995802KH5909Your Name6010Phnom Penh991700131724927295157541100000009800530311662610112TRX0192837750211855123456780305MShop0717Buy 1A_Level_Book63041087

# Generate Deeplink:
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

# Check Transaction paid or unpaid:
payment_status = khqr.check_payment(md5)
print(payment_status)
# String Result: "UNPAID"
# Indicates that this transaction has not yet been paid.

# Retrieve the payment information:
#e.g. In case static QR code (static=True) is used for payment, and the amount is not known from the user's input.
payment_info = khqr.get_payment(md5)
print(payment_info)
# Object Result:
# {
#     "hash": "a7121ca103c.....eb3671b9601a6",
#     "fromAccountId": "bankkhppxxx@bank",
#     "toAccountId": "your_name@bank",
#     "currency": "KHR",
#     "amount": 9800,
#     "description": "Cashier-01",
#     "createdDateMs": 1739###953000,
#     "acknowledgedDateMs": 1739###954000,
#     "trackingStatus": null,
#     "receiverBank": null,
#     "receiverBankAccount": null,
#     "instructionRef": null,
#     "externalRef": "100FT3###6550298"
# }
# You can retrieve information such as the amount to integrate into your system.

# Check Bulk Transactions:
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


# ⚠️ Bulk Transaction Check Limit
# The Bakong API allows a maximum of 50 MD5 hashes per request when using the check_bulk_payments() method.
#If you pass more than 50 hashes, the function will raise a ValueError to prevent unexpected API errors.

md5_list = [md5_1, md5_2, ..., md5_51]  # 51 hashes

# This will raise:
# ValueError: The md5_list exceeds the allowed limit of 50 hashes per request.
result = khqr.check_bulk_payments(md5_list)

# ✅ If you need to check more than 50 transactions, you must handle chunking manually:
def chunked(iterable, size=50):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

all_md5 = [...]  # more than 50 md5 hashes
paid_md5 = []

for batch in chunked(all_md5):
    paid_md5.extend(khqr.check_bulk_payments(batch))

print(paid_md5)
# List Result: ["5154e4f795634ff1a0ae4b48e53a6d9c", "495fdaec0be5d94c89bc1283c7283d3d"]
# Returns a list containing only the MD5 hashes that correspond to successful (paid) transactions.
```

### Generate QR Image

The `qr_image()` method generates a QR code image from a QR string.
Make sure you install the optional [image] extras to get dependencies like Pillow and qrcode:

```bash
pip install bakong-khqr[image]
```

Example:

```bash
from bakong_khqr import KHQR

khqr = KHQR("your_bakong_token")

qr = khqr.create_qr(
    bank_account='user_name@bank',
    merchant_name='Your Name',
    merchant_city='Phnom Penh',
    amount=100.00,
    currency='USD',
    store_label='MShop',
    phone_number='85512345678',
    bill_number='TRX123456',
    terminal_label='Cashier-01',
    static=False
)

# Generate QR image as PNG file path
png_path = khqr.qr_image(qr)
print("QR image saved at:", png_path)

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
- `static`: Static or Dynamic QR code (default: static = False).

`Note`: Using static mode will create a Static QR Code for payment, allowing unlimited transactions, usage, and a zero amount included.

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

#### Parameters for `get_payment()` Method

- `md5`: Valid hash md5 from generate_md5() method of the correct transaction.

#### Parameters for `qr_image()` Method

- `qr`: QR string to convert into an image from create_qr().
- `output_path`: Optional path to save the image. If not provided, returns a temp file path.
- `format`: Image format to export ('png', 'jpeg','webp', 'bytes', 'base64' or 'base64_uri'). Default: 'png'.

## Bakong Official

KHQR SDK Documentation:

- [https://api-bakong.nbc.gov.kh/document](https://api-bakong.nbc.gov.kh/document)
- [KHQR Content Guideline v1.4.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20Content%20Guideline%20v.1.3.pdf)
- [QR Payment Integration.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/QR%20Payment%20Integration.pdf)
- [KHQR SDK Document.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20SDK%20Document.pdf)

Development API: [https://sit-api-bakong.nbc.gov.kh/](https://sit-api-bakong.nbc.gov.kh/)

Production API: [https://api-bakong.nbc.gov.kh/](https://api-bakong.nbc.gov.kh/)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/bsthen/bakong-khqr/blob/main/LICENSE) file for details.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## Contact

For any questions or feedback, you can contact [ME](mailto:bansokthen@gmail.com) or [Buy Me A Coffee ☕️](https://buymeacoffee.com/bsthen)

<p align="center">
        <img src="https://raw.githubusercontent.com/bsthen/bsthen/refs/heads/main/khqr_riel.png" alt="KHQR Donation" width="auto" height="180" style="display: inline-block; margin-right: 10px;">
        <img src="https://raw.githubusercontent.com/bsthen/bsthen/refs/heads/main/khqr_dollar.png" alt="KHQR Donation" width="auto" height="180" style="display: inline-block;">
</p>
