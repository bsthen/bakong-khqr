import os
import unittest
from bakong_khqr.khqr import KHQR
from dotenv import load_dotenv

load_dotenv()

class TestKHQR(unittest.TestCase):
    def setUp(self):
        self.bakong_token = os.getenv("BAKONG_TOKEN")
        if not self.bakong_token:
            raise ValueError("BAKONG_TOKEN is not set in the environment variables.")
        
        # Initialize KHQR with Bakong Token
        self.khqr = KHQR(self.bakong_token)

    def test_create_qr(self):
        
        # Create a QR code string
        qr = self.khqr.create_qr(
            bank_account='sothen_ban@wing',
            merchant_name='Sothen Ban',
            merchant_city='Phnom Penh',
            amount='15',
            currency='USD',
            store_label='Shop A',
            phone_number='85512345678',
            bill_number='TRX019283775',
            terminal_label='Buy Course'
        )
        
        # Get Deeplink
        deeplink = self.khqr.get_deeplink(
            qr, 
            callback="https://bakong.nbc.org.kh", 
            appIconUrl="https://bakong.nbc.gov.kh/images/logo.svg", 
            appName="MyAppName"
        )
        
        # Get Hash MD5
        md5 = self.khqr.get_md5(qr)
        
        # Check transaction paid or unpaid
        is_paid = self.khqr.is_paid(md5)
        
        # print the result
        print("QR Code Data:", qr)
        print("Deeplink:", deeplink)
        print("Hash MD5:", md5)
        print("Is Paid:", is_paid)

if __name__ == '__main__':
    unittest.main()
