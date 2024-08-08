import unittest
from bakong_khqr.khqr import KHQR

class TestKHQR(unittest.TestCase):
    def setUp(self):
        self.khqr = KHQR()

    def test_create_qr(self):
        qr_data = self.khqr.create_qr(
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
        print(f"Generated QR Data: {qr_data}")

if __name__ == '__main__':
    unittest.main()
