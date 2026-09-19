<h1 align="center"> Bakong-KHQR (Unofficial NBC) </h1>

<p align="center">
<a href="https://youtu.be/24bClwP3Tzo" target="_blank" >
        <img src="https://cdn.jsdelivr.net/gh/bsthen/bsthen/dev_qr.png" width="500px" height="492px" alt="YouTube">
    </a>
</p>

> [!TIP]
> **Bakong Relay (bakongrelay.com) is Fully Active & Supported!**  
> You can integrate Bakong KHQR using either an official **NBC Bakong Developer Token** or a **Bakong Relay Token (`rbk...`)**.  
> Register an account, generate store tokens, and manage subscriptions directly via the **Client Portal**: [👉 https://dash.bakongrelay.com](https://dash.bakongrelay.com)

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
        <img src="https://badge.socket.dev/pypi/package/bakong-khqr/0.6.3?artifact_id=tar-gz"
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
      <img src="https://img.shields.io/badge/App_Store-0D96F6?style=flat&logo=app-store&logoColor=white" alt="Apple Store Icon"
           style="vertical-align: middle;" />
  </a> |
  <a href="https://play.google.com/store/apps/details?id=kh.gov.nbc.bakong.tourist" target="_blank">
      <img src="https://img.shields.io/badge/Google_Play-414141?style=flat&logo=Google-play&logoColor=white" alt="Bakong Icon"
           style="vertical-align: middle;" />
  </a>

## 📋 Requirement

- Python 3.8+
- A Bakong account with full KYC verification
- An NBC Bakong Developer Token or a **Bakong Relay Token (`rbk...`)**  
  *(Sign up and generate your token at [dash.bakongrelay.com](https://dash.bakongrelay.com))*

## 📦 Installation

```bash
pip3 install bakong-khqr
```

or Update to the Latest Version:

```bash
pip3 install --upgrade bakong-khqr
```

## 🚀 Key Differences: Bakong Relay vs. NBC Official API

| Feature / Behavior | Bakong Relay (`rbk...` token) | Bakong NBC (Developer Token / Offline) |
| :--- | :--- | :--- |
| **API Endpoint** | `https://api.bakongrelay.com/v1` | `https://api-bakong.nbc.gov.kh/v1` |
| **Hosting & IP Restriction** | **Global Access** (No Cambodia IP restrictions) | Restricted to Cambodia IP addresses |
| **`create_qr()` Requirements** | Only `amount` is strictly required; merchant and currency details are auto-resolved from your RBK Token. | Requires `account_id`, `merchant_name`, `merchant_city`, `amount`, and `currency`. |
| **Amount Validation** | Handled directly by Relay Backend (Min USD $0.01 / Min KHR 100). | Static or Dynamic offline EMVCo generation. |
| **Transaction States** | **4 States:** `PAID`, `SCANNED`, `UNPAID`, `EXPIRED` | **2 States:** `PAID`, `UNPAID` |
| **Polling Optimization** | `SCANNED` = 3s delay; `PAID`/`EXPIRED` = 0s (exit loop). | `PAID` = 0s; `UNPAID` = 5s–300s window matrix. |
| **Gateway Error Handling** | Detailed errors (Token expired/over-limit, Maintenance, Rate limit, Store config). | Standard NBC error messages. |

---

## 💻 Usage Guide

### 1. Using Bakong Relay (`rbk...` Token) — Recommended

When using an `rbk...` token, `create_qr()` only requires `amount`. All merchant and currency details are automatically retrieved from your Store Link configured in the Bakong Relay dashboard.

```python
import time
from bakong_khqr import KHQR

# Initialize with your Bakong Relay Store Token
khqr = KHQR("rbk_live_xxxxxxxxxxxxxxxxxxxx")

# 1. Generate QR Code (amount only; backend auto-detects currency & merchant info)
qr_string = khqr.create_qr(amount=1.50)
print("KHQR String:", qr_string)

# 2. Get MD5 Checksum
md5 = khqr.generate_md5(qr_string)
print("Transaction MD5:", md5)

# 3. Smart Polling Loop (Handles PAID, SCANNED, UNPAID, and EXPIRED)
start_time = time.time()
timeout_seconds = 10 * 60  # 10 minutes

while True:
    status, next_delay = khqr.check_payment(md5, start_time=start_time)
    print(f"Current Status: {status} | Next check in: {next_delay}s")

    if status == "PAID":
        print("🎉 Payment Successful!")
        payment_info = khqr.get_payment(md5)
        print("Transaction Details:", payment_info)
        break

    elif status == "EXPIRED":
        print("❌ Transaction has expired!")
        break

    elif status == "SCANNED":
        print("📱 Customer has scanned the QR. Awaiting PIN/confirmation...")

    # Stop polling if client timeout is reached
    if time.time() - start_time >= timeout_seconds:
        print("🛑 Local polling timeout reached.")
        break

    time.sleep(next_delay)
```

---

### 2. Using Official NBC Token or Offline KHQR Generation

If initialized without a token or with an official NBC Developer Token, the SDK uses the standard EMVCo offline engine:

```python
from bakong_khqr import KHQR

# Without token (Offline EMVCo Generator) or with NBC Token
khqr = KHQR("your_nbc_developer_token_here")

# Full EMVCo parameters are required
qr_string = khqr.create_qr(
    account_id="user_name@bank",
    merchant_name="My Store",
    merchant_city="Phnom Penh",
    amount=10.00,
    currency="USD",
    store_label="Cashier-01",
    phone_number="012345678",
    bill_number="TRX012345",
    terminal_label="POS-01",
    static=False,
    expiration=1
)

md5 = khqr.generate_md5(qr_string)

# Check status via official NBC API (Returns either PAID or UNPAID)
status = khqr.check_payment(md5)
print("Status:", status)
```

---

### 3. Generate Mobile Banking Deeplink

Generate a direct link to open the mobile banking app:

```python
deeplink = khqr.generate_deeplink(
    qr=qr_string,
    appDeepLinkCallback="https://your_website.com/checkout/success](https://your_website.com/checkout/success)",
    appIconUrl="https://your_website.com/images/logo.png](https://your_website.com/images/logo.png)",
    appName="MyStore"
)
print("Deeplink URL:", deeplink)
```

---

### 4. Batch Transaction Verification (`check_bulk_payments`)

Check multiple transactions in a single API call (Maximum 50 hashes per request):

```python
md5_list = [
    "dfcabf4598d1c405a75540a3d4ca099d", 
    "5154e4f795634ff1a0ae4b48e53a6d9c",
    "a57d9bb85f52f12a20cf7beecb03d11d"
]

# Returns a list of MD5 hashes that are confirmed as PAID
paid_hashes = khqr.check_bulk_payments(md5_list)
print("Paid transactions:", paid_hashes)
```

---

### 5. Generate Styled QR Code Image

Install optional dependencies with `pip install "bakong-khqr[image]"`:

```python
# Generate styled KHQR PNG image
image_path = khqr.qr_image(qr_string, format="png")
print("Saved to:", image_path)

# Or export as Base64 Data URI for web embedding
base64_uri = khqr.qr_image(qr_string, format="base64_uri")
print('<img src="' + base64_uri + '" />')
```

---

## 🧠 Smart Polling Guide for `check_payment()`

The `check_payment()` method dynamically adjusts `next_delay` when `start_time` is supplied, preserving API quotas and adapting to customer actions:

| Transaction State | Token Type | Recommended Delay | Explanation |
| :--- | :--- | :--- | :--- |
| **`SCANNED`** | Bakong Relay (`rbk...`) | `3` seconds | Customer has scanned the QR code. Tight polling for instant confirmation. |
| **`PAID`** | Both | `0` seconds | Terminal state. Payment confirmed; break out of the loop immediately. |
| **`EXPIRED`** | Bakong Relay (`rbk...`) | `0` seconds | Terminal state. Session timed out; break out of the loop immediately. |
| **`UNPAID`** (0 – 5 min) | Both | `5` seconds | Active transaction window. High likelihood of scanning. |
| **`UNPAID`** (5 – 15 min) | Both | `10` seconds | Customer might be delayed; reduces request frequency. |
| **`UNPAID`** (15 – 60 min) | Both | `15` seconds | Extended transaction window. |
| **`UNPAID`** (> 60 min) | Both | `300` seconds (5 min) | Dormant or forgotten session; maximum token preservation. |

---

## 🛠️ Method Reference

- **`create_qr(...) -> str`**: Creates an EMVCo-compliant KHQR string. For `rbk` tokens, requests `api.bakongrelay.com`; for NBC tokens or offline use, compiles locally.
- **`generate_md5(qr: str) -> str`**: Computes the 32-character hexadecimal MD5 hash for the QR code.
- **`generate_deeplink(...) -> str | None`**: Generates a mobile banking deep link.
- **`check_payment(md5: str, start_time: float | None = None) -> str | tuple[str, int]`**:
  - Without `start_time`: Returns status string (`PAID`, `SCANNED`, `UNPAID`, `EXPIRED`).
  - With `start_time`: Returns `(status, next_delay)` tuple.
- **`get_payment(md5: str) -> dict | None`**: Returns transaction details if confirmed `PAID`. Returns `None` if `SCANNED`, `UNPAID`, or `EXPIRED`.
- **`check_bulk_payments(md5_list: list[str]) -> list[str]`**: Verifies an array of MD5 hashes (Max 50) and returns a list of paid hashes.
- **`qr_image(qr: str, format: str = "png", output_path: str | None = None) -> str | bytes`**: Exports styled KHQR image in PNG, JPEG, WebP, raw bytes, Base64, or Data URI format.

---

## ⚠️ Web Checkout Integration (Coming soon)

> [!IMPORTANT]
> Hosted Web Checkout features (`create_webcheckout()` and `get_webcheckout()`) require an active **Bakong Relay Token (`rbk...`)**.  
> We are developing this feature.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/bsthen/bakong-khqr/blob/main/LICENSE) file for details.

## 📬 Contact & Support

- **Author**: BAN Sothen
- **Email**: [bansokthen@gmail.com](mailto:bansokthen@gmail.com)
- **Telegram Support**: [@bakongRelaySupport](https://t.me/bakongRelaySupport/)
- **Buy Me a Coffee**: [buymeacoffee.com/bsthen](https://buymeacoffee.com/bsthen)

<p align="center">
    <img src="https://cdn.jsdelivr.net/gh/bsthen/bsthen@main/khqr_riel.png" alt="KHQR Donation" width="auto" height="250" style="display: inline-block; margin-right: 10px;">
    <img src="https://cdn.jsdelivr.net/gh/bsthen/bsthen@main/khqr_dollar.png" alt="KHQR Donation" width="auto" height="250" style="display: inline-block;">
</p>

## ❤️ Sponsors

This project is supported by the community.  
👉 [List Sponsors & Donors](https://github.com/bsthen/bakong-khqr/blob/main/SPONSORS.md)
