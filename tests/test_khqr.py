import os
import unittest
from bakong_khqr.khqr import KHQR
from dotenv import load_dotenv

load_dotenv()

class TestKHQR(unittest.TestCase):
    def setUp(self):
        self.__bakong_token = os.getenv("BAKONG_TOKEN")
        if not self.__bakong_token:
            raise ValueError("BAKONG_TOKEN is not set in the environment variables.")
        
        # Initialize KHQR with Bakong Token
        self.khqr = KHQR(self.__bakong_token)

    def test_create_qr(self):
        
        # Create a QR code string
        qr = self.khqr.create_qr(
            bank_account='your_name@bank', # Check your user_name@bank under Bakong profile (Mobile App)
            merchant_name='YOUR NAME', # Merchant name (e.g., Your Name)
            merchant_city='Phnom Penh', # City name (e.g., Phnom Penh)
            amount=9800, #9800 Riel
            currency='KHR', # USD or KHR
            store_label='Phsar Thmei', # Store label or transaction description (e.g., Buy Course)
            phone_number='012345678', # Customer's phone number (e.g., 012345678). This is used for the "Pay by Phone Number" feature in the Bakong app.
            bill_number='TRX012345', # Bill number or transaction reference (e.g., TRX019283775).
            terminal_label='POS-01', # Terminal label or transaction description (e.g., Buy Course).
            static=False, # Static or Dynamic QR code (default: False)
            expiration=2 # Expiration time in 2 days for the QR code (default: 1 day). This is used to calculate the expiration time for the QR code.
        )
        
        print("QR Code Data:", qr)
        # Get Deeplink URL for the QR code
        deeplink = self.khqr.generate_deeplink(
            qr, 
            callback="https://bakong.nbc.org.kh", 
            appIconUrl="https://bakong.nbc.gov.kh/images/logo.svg", 
            appName="MyAppName"
        )
        
        # Get Hash MD5
        md5 = self.khqr.generate_md5(qr)
        
        # Check transaction paid or unpaid
        payment_status = self.khqr.check_payment(md5)
        
        # Retrieve the payment information
        payment_info = self.khqr.get_payment(md5)
        
        # Check Bulk Transactions
        md5_list = [
            "dfcabf4598d1c405a75540a3d4ca099d", 
            "5154e4f795634ff1a0ae4b48e53a6d9c",
            "a57d9bb85f52f12a20cf7beecb03d11d",
            "495fdaec0be5d94c89bc1283c7283d3d",
            "31bca02094ad576588e42b60db57bc98"
        ]
        bulk_payments_status = self.khqr.check_bulk_payments(md5_list)
        
        # print the result
        print("QR Code Data:", qr)
        print("Deeplink:", deeplink)
        print("Transaction MD5:", md5)
        print("Check Payment Status:", payment_status)
        print("Payment Information:", payment_info)
        print("Check Bulk Payments Status:", bulk_payments_status)

if __name__ == '__main__':
    unittest.main()
