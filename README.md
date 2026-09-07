<h1 align="center"> Bakong-KHQR (Unofficial NBC) </h1>

<p align="center">
<a href="https://youtu.be/24bClwP3Tzo" target="_blank" >
        <img src="https://cdn.jsdelivr.net/gh/bsthen/bsthen/dev_qr.png" width="500px" heigh="492px" alt="YouTube">
    </a>
</p>

> [!IMPORTANT]
> **Bakong Relay (bakongrelay.com) Discontinued Notice**  
> The hosted relay service (~~https://bakongrelay.com~~) and RBK tokens have been discontinued.  
> **The core `bakong-khqr` Python SDK remains active and maintained** for generating KHQR strings, Deeplinks, MD5 transaction hashes, QR images, and checking transactions directly using official NBC Bakong tokens (`api-bakong.nbc.gov.kh`).

<p align="center">
A Python package for generating payment transactions compliant with the Bakong KHQR standard.
</p>

<p align="center">
    <a href="https://opensource.org/licenses/MIT" target="_blank" >
        <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
    </a>
    <a href="https://pypi.org/project/bakong-khqr/" target="_blank" >
        <img src="https://img.shields.io/pypi/pyversions/bakong-khqr.svg" alt="Python Version">
    </a>
    <a href="https://pypi.org/project/bakong-khqr/" target="_blank" >
        <img src="https://img.shields.io/pypi/v/bakong-khqr?color=%2334D058&label=pypi%20package" alt="PyPI version">
    </a>
    <a href="https://socket.dev/pypi/package/bakong-khqr/" target="_blank">
        <img src="https://badge.socket.dev/pypi/package/bakong-khqr/0.6.0?artifact_id=tar-gz"
             alt="Socket Security">
    </a>
    <a href="https://pepy.tech/projects/bakong-khqr" target="_blank" >
        <img src="https://static.pepy.tech/badge/bakong-khqr" alt="Downloads">
    </a>
</p>

## 📱 Download Mobile App

- <img src="https://cdn.jsdelivr.net/gh/bsthen/bsthen/bakong_app.png"
       alt="Bakong App"
       width="28"
       style="vertical-align: middle;" />
  <strong style="margin: 0 6px;">Bakong App</strong>
  <a href="https://apps.apple.com/kh/app/bakong/id1440829141" target="_blank">
      <img src="https://img.shields.io/badge/App_Store-0D96F6?style=flat&logo=app-store&logoColor=white" alt="Apple Store Icon"
           style="vertical-align: middle;" />
  </a> |
  <a href="https://play.google.com/store/apps/details?id=jp.co.soramitsu.bakong" target="_blank">
      <img src="https://img.shields.io/badge/Google_Play-414141?style=flat&logo=google-play&logoColor=white" alt="Google Play Icon"
           style="vertical-align: middle;" />
  </a>

- <img src="https://cdn.jsdelivr.net/gh/bsthen/bsthen/bakong_tourists.png"
       alt="Bakong Tourists"
       width="28"
       style="vertical-align: middle;" />
  <strong style="margin: 0 6px;">Bakong Tourists</strong>
  <a href="https://apps.apple.com/kh/app/bakong-tourists/id6471774666" target="_blank">
      <img src="https://img.shields.io/badge/App_Store-0D96F6?style=flat&logo=app-store&logoColor=white" alt="Bakong Tourists Icon"
           style="vertical-align: middle;" />
  </a> |
  <a href="https://play.google.com/store/apps/details?id=kh.gov.nbc.bakong.tourist" target="_blank">
      <img src="https://img.shields.io/badge/Google_Play-414141?style=flat&logo=google-play&logoColor=white" alt="Bakong Icon"
           style="vertical-align: middle;" />
  </a>

## 📋 Requirement

- Python 3.8+
- A Bakong account with full KYC verification
- A Bakong developer token (register here: [https://api-bakong.nbc.gov.kh/register/](https://api-bakong.nbc.gov.kh/register/))
- A VPS or hosting service located in Cambodia (required by NBC to query official Bakong APIs without HTTP 403 errors).
- *(Note: RBK Token & ~~https://bakongrelay.com~~ have been discontinued).*

## 📦 Installation

```bash
pip3 install bakong-khqr
```

or Update Last Version

```bash
pip3 install --upgrade bakong-khqr
```

## 🚀 Usage

The bakong-khqr package provides the `KHQR` class for generating QR codes, Deeplinks, MD5 hashes, and verifying Bakong KHQR transactions.

### Importing the package

You can import the KHQR class from the package as follows:

```python
from bakong_khqr import KHQR
```

### Creating Payment Transaction

To generate QR code data for a transaction, create an instance of the `KHQR()` class with your official Bakong Token:

- `create_qr()` method with the required parameters.
- `generate_deeplink()` method with the required parameters.
- `generate_md5()` method with the required parameters.
- `check_payment()` method with the required parameters.
- `get_payment()` method with the required parameters.
- `check_bulk_payments()` method with the required parameters.

#### 🔄 Parameter Update Notice (`bank_account` ➡️ `account_id`)

To align perfectly with the official Bakong documentation, the parameter `bank_account` has been renamed to `account_id`.

- Backward Compatibility: If your old code still uses `bank_account`, it will continue to work normally but a `DeprecationWarning` will be triggered. It is highly recommended to update your codebase to use `account_id`.

Example:

```python
from bakong_khqr import KHQR

# Create an instance of KHQR with Bakong Developer Token:
khqr = KHQR("eyJhbGciOiJIUzI1NiIsI...nMhgG87BWeDg9Lu-_CKe1SMqC0")

# Generate QR code data for a transaction:
qr_string = khqr.create_qr(
    account_id='user_name@bank', # Check your user_name@bank under Bakong profile (Mobile App)
    merchant_name='Your Name',
    merchant_city='Phnom Penh',
    amount=9800, # 9800 Riel
    currency='KHR', # USD or KHR
    store_label='Phsar Thmei',
    phone_number='012345678',
    bill_number='TRX012345',
    terminal_label='POS-01',
    static=False, # Static or Dynamic QR code (default: False)
    expiration=1 # Expiration time in 1 day for the QR code (default: 1 day).
)
print(qr_string)
# String Result: 00020101021229180014your_name@bank520459995303116540498005802KH5909Your Name6010Phnom Penh62510109TRX01234502090123456780311Phsar Thmei0706POS-01993400131773894603019011317738947758196304A5A3

# Generate Deeplink:
deeplink = khqr.generate_deeplink(
    qr=qr_string,
    appDeepLinkCallback="https://your_website.com/shop/details?q=ABC", # Or your app's custom scheme (e.g., mshop://purchase/39482)
    appIconUrl="https://your_website.com/images/logo.png", # Your logo image .png or .svg
    appName="MyAppName" # (e.g., MSHOP)
)
print(deeplink)
# String Result: https://bakong.page.link/CgXb....ks6az9a38

# Get Hash MD5
md5 = khqr.generate_md5(qr_string)
print(md5)
# String Result: dfcabf4598d1c405a75540a3d4ca099d

# Check Transaction paid or unpaid:
payment_status = khqr.check_payment(md5)
print(payment_status)
# String Result: "UNPAID"
# Indicates that this transaction has not yet been paid.

# Retrieve the payment information:
# e.g. In case static QR code (static=True) is used for payment, and the amount is not known from the user's input.
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
# If you pass more than 50 hashes, the function will raise a ValueError to prevent unexpected API errors.

# ✅ If you need to check more than 50 transactions, handle chunking manually:
def chunked(iterable, size=50):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

all_md5 = [...]  # more than 50 md5 hashes
paid_md5 = []

for batch in chunked(all_md5):
    paid_md5.extend(khqr.check_bulk_payments(batch))

print(paid_md5)
```

### 🖼️ Generate QR Image

The `qr_image()` method generates a QR code image from a QR string.
Make sure you install the optional `[image]` extras to get dependencies like Pillow and qrcode:

```bash
pip3 install "bakong-khqr[image]"
```

Example:

```python
from bakong_khqr import KHQR

khqr = KHQR("your_bakong_token")

qr = khqr.create_qr(
    account_id='user_name@bank',
    merchant_name='Your Name',
    merchant_city='Phnom Penh',
    amount=100.00,
    currency='USD',
    store_label='MShop',
    phone_number='85512345678',
    bill_number='TRX123456',
    terminal_label='Cashier-01',
    static=False,
    expiration=1
)

# Generate QR image as PNG file path
png_path = khqr.qr_image(qr)
print("QR image saved at:", png_path)
```

---

### ⚠️ Web Checkout Integration (Discontinued)

> [!CAUTION]
> Hosted Web Checkout and RBK tokens via ~~https://bakongrelay.com~~ have been **discontinued**.
> Methods `create_webcheckout()` and `get_webcheckout()` are no longer supported. Please integrate directly using official NBC KHQR payloads and mobile deeplinks.

---

#### Parameters for `create_qr()` Method

- `account_id`: The Bakong Account ID associated with the transaction.
- `merchant_name`: Name of the merchant.
- `merchant_city`: City where the merchant is located.
- `amount`: Amount to be transacted.
- `currency`: Currency of the transaction (e.g., 'USD', 'KHR').
- `store_label` (optional): Label or name of the store.
- `phone_number` (optional): Contact phone number.
- `bill_number` (optional): Reference number for the bill.
- `terminal_label` (optional): Label for the terminal.
- `static` (optional): Static or Dynamic QR code (default: static = False).
- `expiration` (optional): Expiration time in days for the QR code (default: 1 day).

`Note`: Using static mode will create a Static QR Code for payment, allowing unlimited transactions, usage, and a zero amount included.

#### Parameters for `generate_deeplink()` Method

- `qr`: Valid QR Code data as string that generate from create_qr() method.
- `appDeepLinkCallback`: Deeplink URL for opening your app after payment is completed.
- `appIconUrl`: Your App Icon URL.
- `appName`: Your App Name.

    ***Deprecation Note***: The parameter `callback` has been renamed to `appDeepLinkCallback` to align with the Bakong standard. While `callback` still works for backward compatibility, it will be removed in future releases.

#### Parameters for `generate_md5()` Method

- `qr`: Valid QR Code data as string that generate from create_qr() method.

#### Parameters for `check_payment()` Method

- `md5`: Valid hash md5 from generate_md5() method of the correct transaction.
- `start_time`: (float, optional): The timestamp (time.time()) when the transaction or QR code was created. If provided, returns a tuple containing the `status` and the suggested `next delay`.

#### Parameters for `check_bulk_payments()` Method

- `md5_list`: md5 list of all transactions generate from generate_md5() method.

#### Parameters for `get_payment()` Method

- `md5`: Valid hash md5 from generate_md5() method of the correct transaction.

#### Parameters for `qr_image()` Method

- `qr`: QR string to convert into an image from create_qr().
- `output_path`: Optional path to save the image. If not provided, returns a temp file path.
- `format`: Image format to export ('png', 'jpeg','webp', 'bytes', 'base64' or 'base64_uri'). Default: 'png'.

# ✨ What's New?

## 1. ⚡ Bakong Relay API *(Discontinued)*

> [!NOTE]
> The hosted service at ~~bakongrelay.com~~ has been discontinued. Developers should use official Bakong developer tokens from the National Bank of Cambodia directly from servers hosted within Cambodia.

## 2. 🧠 Smart Polling Guide for `check_payment()`

Starting from version `0.6.0+`, the `check_payment()` method supports a smart Dynamic Polling Delays Matrix. This optimizes API token consumption and prevents server overload, while remaining 100% non-blocking and safe for Single-Threaded systems (like standard Telegram Bots).

### 1. How it works (The Concept)

- **Legacy Flow (Backward Compatible)**: If you call `check_payment(md5)` without any extra parameters, it behaves exactly like the old version. It makes one API request and immediately returns a string (`"PAID"` or `"UNPAID"`).

- **Smart Polling Flow**: If you provide the `start_time` parameter, the SDK will not block or loop internally. Instead, it will instantly check the status and suggest a recommended wait time (`next_delay` in seconds) based on how long the QR code has been open.

### 2. 💻 Code Implementation (How Merchants Should Write the Loop)

Below are practical examples of how developers can implement the check loop in their applications.

**❌ The Bad Way (Legacy Loop - High Token Consumption)**:

Previously, developers used a fixed loop interval. This bursts API endpoints and burns tokens rapidly, especially if a customer leaves the QR screen open for hours.

```python
import time
from bakong_khqr import KHQR

khqr = KHQR("your_token")
md5 = "your_transaction_md5"

# 1. Mark the starting time and set a 10-minute timeout (600 seconds)
start_time = time.time()
timeout_seconds = 10 * 60

print("Polling started with a 10-minute timeout...")

while True:
    status = khqr.check_payment(md5)
    
    if status == "PAID":
        print("Success!")
        break
        
    # Calculate how much time has passed
    elapsed_time = time.time() - start_time
    
    # 2. Force break the loop once 10 minutes have passed
    if elapsed_time >= timeout_seconds:
        print("Timeout reached. Transaction expired!")
        break
        
    time.sleep(1)

# ❌ BAD: Hardcoded 1-second interval will waste up to 600 API calls in 10 minutes!
```

**✅ The Best Way (Smart Polling with Timeout Control)**:

This approach tells the SDK exactly when the QR code session started. The SDK returns a recommended delay matching your platform's dynamic windows matrix, while the loop cleanly handles its own expiration timeout.

```python
import time
from bakong_khqr import KHQR

khqr = KHQR("your_token")
md5 = "your_transaction_md5"

# 1. Mark the starting time of the transaction session
start_time = time.time()

# 2. Set your custom expiration timeout (e.g., 10 minutes)
timeout_minutes = 10
timeout_seconds = timeout_minutes * 60

print(f"Polling started. Expiration set to {timeout_minutes} minutes.")

# 3. Non-blocking smart loop
while True:
    # Pass start_time to get the status alongside a recommended dynamic delay
    status, next_delay = khqr.check_payment(md5, start_time=start_time)
    
    # Condition A: Payment is successful -> Break out immediately
    if status == "PAID":
        print("🎉 Payment Successful! Processing order...")
        break
        
    # Calculate total seconds elapsed since the QR was created
    elapsed_time = time.time() - start_time
    
    # Condition B: Reached maximum expiration limit -> Stop polling safely
    if elapsed_time >= timeout_seconds:
        print("🛑 Timeout reached. Transaction expired.")
        break
        
    # Condition C: Still UNPAID -> Wait exactly as suggested by the SDK matrix
    print(f"Status: UNPAID. Sleeping for {next_delay}s...")
    time.sleep(next_delay)

# ✅ GOOD: Smart dynamic delay will only use up to 90 API calls in 10 minutes!
```

### 📊 Understanding the Response Matrix

When `start_time` is passed, the SDK dynamically adjusts `next_delay` according to this timeline to balance swift notifications with API efficiency:

| Time Elapsed since Start | SDK Recommended Delay | Total Calls Made (if Unpaid) | Why? |
| --------- | ------------------ | ------------------ | ------------------ |
| 0 to 5 minutes | `5` seconds | Up to 60 calls | High chance of instant scanning. Keeps it snappy. |
| 5 to 15 minutes | `10` seconds | Up to 60 calls | Customer might be delayed. Ease up on the requests. |
| 15 minutes to 1 hour | `15` seconds | Up to 180 calls | Extended window. Further reduces token consumption. |
| Over 1 hour | `300` seconds (5 mins) | 12 calls / hour | Dormant or forgotten QR session. Maximum preservation. |

### 🛠️ Method Signature Breakdown

```python
def check_payment(self, md5: str, start_time: float = None) -> str | tuple[str, int]:
```

- Parameters:
  - `md5` *(str)*: Valid hash MD5 from `generate_md5()`.
  - `start_time` *(float, optional)*: The Unix timestamp generated by `time.time()` when the QR code transaction was initialized.

- Return Values:
  - Returns `str` (e.g., `"UNPAID"`) if `start_time` is omitted.
  - Returns `tuple` (e.g., `("UNPAID", 5)`) if `start_time` is supplied.

## 📄 Bakong Official

KHQR SDK Documentation:

- [https://api-bakong.nbc.gov.kh/document](https://api-bakong.nbc.gov.kh/document)
- [KHQR Content Guideline v1.4.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20Content%20Guideline%20v.1.3.pdf)
- [QR Payment Integration.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/QR%20Payment%20Integration.pdf)
- [KHQR SDK Document.pdf](https://bakong.nbc.gov.kh/download/KHQR/integration/KHQR%20SDK%20Document.pdf)

Development API: [https://sit-api-bakong.nbc.gov.kh/](https://sit-api-bakong.nbc.gov.kh/)

Production API: [https://api-bakong.nbc.gov.kh/](https://api-bakong.nbc.gov.kh/)

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/bsthen/bakong-khqr/blob/main/LICENSE) file for details.

## 🤝 Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request.

## 📬 Contact

For any questions or feedback, you can contact me via [Mail](mailto:bansokthen@gmail.com), [Telegram](https://t.me/bakongRelaySupport/) or [Buy Me A Coffee ☕️](https://buymeacoffee.com/bsthen)

<p align="center">
        <img src="https://cdn.jsdelivr.net/gh/bsthen/bsthen@main/khqr_riel.png" alt="KHQR Donation" width="auto" height="250" style="display: inline-block; margin-right: 10px;">
        <img src="https://cdn.jsdelivr.net/gh/bsthen/bsthen@main/khqr_dollar.png" alt="KHQR Donation" width="auto" height="250" style="display: inline-block;">
</p>

## ❤️ Sponsors

This project is supported by the community.  
👉 [List Sponsors & Donors](https://github.com/bsthen/bakong-khqr/blob/main/SPONSORS.md)
