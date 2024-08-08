import unittest
from bakong_khqr.khqr import KHQR

class TestKHQR(unittest.TestCase):
    def setUp(self):
        self.khqr = KHQR()

    def test_create_qr(self):
        qr_data = self.khqr.create_qr(
            bank_account="sothen_ban@wing",
            merchant_name="Sothen Ban",
            merchant_city="Phnom Penh",
            amount=1.00,
            currency="USD",
            store_label="Store A",
            phone_number="123456789",
            bill_number="TRX01876883",
            terminal_label="Terminal 1"
        )
        print(f"Generated QR Data: {qr_data}")
        # self.assertIn('1.00', qr_data)

if __name__ == '__main__':
    unittest.main()
