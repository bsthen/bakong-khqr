# bakong-khqr

[![PyPI version](https://img.shields.io/pypi/v/bakong-khqr.svg)](https://pypi.org/project/bakong-khqr/)
[![Python versions](https://img.shields.io/pypi/pyversions/bakong-khqr.svg)](https://pypi.org/project/bakong-khqr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, robust Python library for generating EMVCo-compliant **Bakong KHQR** strings, checking transaction payment statuses, generating mobile banking deep links, and rendering styled QR images.

---

## Features

- **Offline / Local Generation**: Generate valid EMVCo KHQR payloads locally without external network dependencies.
- **Custom Gateway Integration**: Easily connect to custom or self-hosted payment relay endpoints via `base_url` and `KHQRConfig`.
- **Backward Compatible**: Seamlessly supports existing implementations and legacy token methods without breaking changes.
- **Smart Polling**: Adaptive interval calculation to verify payment statuses while optimizing API requests.
- **Bulk Verification**: Check up to 50 transactions simultaneously in a single API call.
- **Mobile Deep Linking**: Generate direct URLs to launch mobile banking apps on smartphones.
- **Built-in Image Tools**: Render official-style KHQR templates as PNG, JPEG, WebP, or Base64 Data URIs (optional extra).

---

## Installation

### Standard Installation
```bash
pip install bakong-khqr
```

### Installation with Image Generation Support
If you plan to use `qr_image()` to generate styled PNG/JPEG images:
```bash
pip install "bakong-khqr[image]"
```

---

## Initialization & Configuration

`KHQR` can be initialized in multiple flexible ways depending on your architectural setup:

### 1. Custom Gateway / Relay Mode (Recommended for Custom API Servers)
If you deploy your own relay API server or use a custom endpoint, specify `base_url`:

#### Option A: Using `KHQRConfig` Dataclass
```python
from bakong_khqr import KHQR, KHQRConfig

config = KHQRConfig(
    token="your_api_token",
    base_url="https://api.yourgateway.com/v1"
)
khqr = KHQR(config=config)
```

#### Option B: Using Direct Arguments
```python
from bakong_khqr import KHQR

khqr = KHQR(
    token="your_api_token",
    base_url="https://api.yourgateway.com/v1"
)
```

### 2. Standard Official NBC Mode
For standard offline QR generation or connecting directly to official endpoints:
```python
from bakong_khqr import KHQR

khqr = KHQR("your_bakong_token_here")
```

---

## Quickstart & Usage Examples

### 1. Generating a KHQR Code

#### A. Gateway / Relay Mode
When using a configured `base_url`, merchant credentials and currency can be resolved on the server side:
```python
from bakong_khqr import KHQR, KHQRConfig

config = KHQRConfig(
    token="your_token",
    base_url="https://api.yourgateway.com/v1"
)
khqr = KHQR(config=config)

response = khqr.create_qr(
    amount=10.0,
    return_url="https://yourstore.com/checkout/return",
    bill_number="INV-2026-001"
)

# KHQRResponse acts directly as the raw QR string:
print("QR Code:", response)
print("MD5 Checksum:", response.md5)
print("Transaction ID:", response.tran_id)
print("Checkout URL:", response.checkout_url)
```

#### B. Offline / Direct EMVCo Generation
Generate QR strings locally by supplying complete merchant specifications:
```python
from bakong_khqr import KHQR

khqr = KHQR()

qr_string = khqr.create_qr(
    account_id="merchant_name@bank",
    merchant_name="Sample Store",
    merchant_city="Phnom Penh",
    amount=15000,
    currency="KHR",
    bill_number="TRX-1002"
)

print("Generated KHQR:", qr_string)
```

---

### 2. Checking Payment Status & Smart Polling

Verify whether a payment has been captured using the 32-character MD5 checksum.

#### Single Status Check
```python
md5_hash = khqr.generate_md5(qr_string)

status = khqr.check_payment(md5_hash)
print("Payment Status:", status)
# Returns: 'PAID', 'SCANNED', 'EXPIRED', or 'UNPAID'
```

#### Smart Polling Loop (Optimized Polling Overhead)
Pass `start_time` into `check_payment()` to dynamically calculate the optimal sleep delay:
```python
import time

start_time = time.time()
timeout_seconds = 10 * 60  # 10 minutes

while True:
    status, next_delay = khqr.check_payment(md5_hash, start_time=start_time)

    if status == "PAID":
        print("Payment Confirmed!")
        # Fulfill order here
        break

    if status == "EXPIRED" or (time.time() - start_time) >= timeout_seconds:
        print("Payment session expired.")
        break

    time.sleep(next_delay)
```

---

### 3. Retrieving Confirmed Transaction Details

Retrieve payment receipt information once a transaction is completed:
```python
payment_info = khqr.get_payment(md5_hash)

if payment_info:
    print("Amount Paid:", payment_info.get("amount"))
    print("Currency:", payment_info.get("currency"))
    print("Payer Bank:", payment_info.get("payerBank"))
```

---

### 4. Bulk Payment Status Verification

Verify up to 50 transactions simultaneously in one network call:
```python
md5_list = [
    "c4ca4238a0b923820dcc509a6f75849b",
    "c81e728d9d4c2f636f067f89cc14862c",
    "eccbc87e4b5ce2fe28308fd9f2a7baf3"
]

paid_md5s = khqr.check_bulk_payments(md5_list)
print("Paid Transactions:", paid_md5s)
```

---

### 5. Mobile Deep Link Generation

Generate deep links to open mobile banking applications directly:
```python
deeplink = khqr.generate_deeplink(
    qr=qr_string,
    appName="MyStoreApp",
    appIconUrl="https://mystore.com/icon.png",
    appDeepLinkCallback="https://mystore.com/orders/verify"
)

print("Mobile Deep Link:", deeplink)
```

---

### 6. Styled KHQR Image Generation

Render branded KHQR templates locally as files or Base64 URIs:

```python
# Save as a PNG file
png_path = khqr.qr_image(qr_string, format="png", output_path="checkout_qr.png")

# Output as Base64 Data URI (ideal for web embedding)
base64_data_uri = khqr.qr_image(qr_string, format="base64_uri")
print('<img src="' + base64_data_uri + '" alt="Scan to Pay" />')
```

Supported formats: `png`, `jpeg`, `webp`, `bytes`, `base64`, `base64_uri`.

---

## API Reference

### `KHQRConfig` (Dataclass)

| Field | Type | Default | Description |
|---|---|---|---|
| `token` | `str \| None` | `None` | Authentication Bearer token. |
| `base_url` | `str \| None` | `None` | Base URL for custom relay/gateway endpoints. |

### `KHQR(bakong_token=None, base_url=None, token=None, config=None)`

- **`config`** (`KHQRConfig`, optional): Configuration instance containing `token` and `base_url`.
- **`token`** (`str`, optional): API Bearer token.
- **`base_url`** (`str`, optional): Custom Gateway base URL (e.g., `https://api.yourgateway.com/v1`).
- **`bakong_token`** (`str \| KHQRConfig`, optional): Positional token for backward compatibility.

### `create_qr(...)` Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount` | `float` | Yes | Transaction amount (`>= 0.01` USD, `>= 100` KHR). |
| `return_url` | `str \| None` | No | Destination URL after checkout completion. |
| `success_url` | `str \| None` | No | Redirect destination specifically upon successful payment. |
| `cancel_url` | `str \| None` | No | Redirect destination if cancelled or expired. |
| `account_id` | `str \| None` | Conditional | Payee account identifier (e.g. `merchant@bank`). |
| `merchant_name` | `str \| None` | Conditional | Merchant display name. |
| `merchant_city` | `str \| None` | Conditional | Merchant location city (default: `Phnom Penh`). |
| `currency` | `str \| None` | Conditional | Currency code (`USD` or `KHR`). |
| `bill_number` | `str \| None` | No | Order / Invoice reference identifier. |
| `store_label` | `str \| None` | No | Branch / store description. |
| `phone_number` | `str \| None` | No | Contact phone number. |
| `terminal_label` | `str \| None` | No | Terminal identifier. |
| `static` | `bool` | No | Generate static QR (no fixed amount). Default: `False`. |
| `expiration` | `int` | No | Expiration duration in days. Default: `1`. |
| `return_dict` | `bool` | No | Return raw dictionary instead of `KHQRResponse`. |

---

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This package is an independent open-source project and is not affiliated with, officially endorsed by, or authorized by the National Bank of Cambodia (NBC).