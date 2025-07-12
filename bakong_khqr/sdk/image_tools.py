import os
import io
import base64
import tempfile
from importlib import resources
from .emv_parser import EMVParser

class ImageTools:
    def __init__(self):
        self.__regular_font = resources.files("bakong_khqr.sdk.assets").joinpath("regular.ttf").read_bytes()
        self.__bold_font = resources.files("bakong_khqr.sdk.assets").joinpath("bold.ttf").read_bytes()
        self.__khqr_logo = resources.files("bakong_khqr.sdk.assets").joinpath("logo.png").read_bytes()
        self.__usd_icon = resources.files("bakong_khqr.sdk.assets").joinpath("USD.png").read_bytes()
        self.__khr_icon = resources.files("bakong_khqr.sdk.assets").joinpath("KHR.png").read_bytes()
        
    def __format_amount(self, amount: float, currency: str) -> str:
        # Format amount based on currency
        if currency.upper() == "USD":
            parts = f"{amount:,.2f}".split(".")
            grouped = parts[0].replace(",", ".")
            return f"{grouped},{parts[1]}"
        else:
            return f"{amount:,.2f}"
        
    def __draw_red_corner(self, draw, width, height, fold_size=40, color="#cc0000"):
    # Top-right triangle (fold)
        triangle = [
            (width - fold_size, 0),       # top edge left of corner
            (width, 0),                   # top-right corner
            (width, fold_size)           # right edge below corner
        ]
        draw.polygon(triangle, fill=color)


    def __add_rounded_corners(self, image, radius):
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            raise ImportError("Image processing requires: pip install 'bakong-khqr[image]'")
        
        width, height = image.size
        # Create a mask
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=255)
        
        # Apply mask to image
        rounded = Image.new("RGBA", (width, height))
        rounded.paste(image, (0, 0), mask)
        return rounded

    def __draw_dashed_line(self, draw, start, end, dash_length=5, gap_length=5, fill="black", width=1):
        x1, y1 = start
        x2, y2 = end
        total_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        dx = (x2 - x1) / total_length
        dy = (y2 - y1) / total_length

        drawn = 0
        while drawn < total_length:
            x_start = x1 + dx * drawn
            y_start = y1 + dy * drawn
            drawn += dash_length
            x_end = x1 + dx * min(drawn, total_length)
            y_end = y1 + dy * min(drawn, total_length)
            draw.line([(x_start, y_start), (x_end, y_end)], fill=fill, width=width)
            drawn += gap_length
    
    def generate(self, qr_string):
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            import qrcode
            import qrcode.constants
        except ImportError:
            raise ImportError("Image processing requires: pip install 'bakong-khqr[image]'")
        
        merchant_name_font = ImageFont.truetype(io.BytesIO(self.__regular_font), 16)
        bold_amount_font = ImageFont.truetype(io.BytesIO(self.__bold_font), 22)
        regular_currency_font = ImageFont.truetype(io.BytesIO(self.__regular_font), 14)
        
        bakong_logo = Image.open(io.BytesIO(self.__khqr_logo)).convert("RGBA")
        usd_icon = Image.open(io.BytesIO(self.__usd_icon)).convert("RGBA")
        khr_icon = Image.open(io.BytesIO(self.__khr_icon)).convert("RGBA")
        
        # Get the EMV data from the QR string
        emv = EMVParser(qr_string)
        merchant_name = emv.get("59") or "Unknown"
        amount = float(emv.get("54") or "0")
        currency_code = emv.get("53") or "840"
        currency = "USD" if currency_code == "840" else "KHR"
        
        # Step 1: Generate QR code
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10, border=4)
        qr.add_data(qr_string)
        qr.make()
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_img = qr_img.resize((280, 280))

        # Step 2: Create template image
        width, height = 300, 450
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Red header
        draw.rectangle([(0, 0), (width, 60)], fill=(204, 0, 0))

        # KHQR logo
        khqr_logo = bakong_logo.resize((90, 21))
        img.paste(khqr_logo, (width // 2 - 40, 20), khqr_logo)

        # Merchant name, amount, currency with loaded fonts
        draw.text((32, 80), merchant_name, fill="black", font=merchant_name_font)
        
        # Format amount and measure its width
        amount_text = self.__format_amount(amount, currency)
        
        # Use a dummy draw object to measure text
        dummy_img = Image.new("RGB", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)

        # Get bounding box of the amount text
        bbox = dummy_draw.textbbox((0, 0), amount_text, font=bold_amount_font)
        amount_width = bbox[2] - bbox[0]  # right - left

        # Draw amount
        draw.text((30, 110), amount_text, fill="black", font=bold_amount_font)

        # Draw currency next to amount
        currency_x = 30 + amount_width + 5
        draw.text((currency_x, 118), currency, fill="black", font=regular_currency_font)


        # Dashed line
        self.__draw_dashed_line(draw, (0, 150), (340, 150), dash_length=2, gap_length=4, fill="grey", width=1)

        # Paste QR code
        img.paste(qr_img, (10, 160))

        # Currency icon
        currency_icon = usd_icon if currency == "USD" else khr_icon
        currency_icon = currency_icon.resize((40, 40))
        img.paste(currency_icon, (width // 2 - 20, 280), currency_icon)

        # Draw red corner & round corners
        self.__draw_red_corner(draw, width, height, fold_size=90)
        rounded_img = self.__add_rounded_corners(img, radius=15)

        # Return wrapped result
        return QRImageResult(rounded_img)
    
class QRImageResult:
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Image processing requires: pip install 'bakong-khqr[image]'")
    
    def __init__(self, image: Image.Image):
        self.image = image

    def to_png(self, path: str = None) -> str:
        if path is None:
            path = os.path.join(tempfile.gettempdir(), "khqr_image.png")
        self.image.save(path, format="PNG")
        return path
    
    def to_jpeg(self, path: str = None) -> str:
        if path is None:
            path = os.path.join(tempfile.gettempdir(), "khqr_image.jpg")
        self.image.convert("RGB").save(path, format="JPEG")
        return path
    
    def to_webp(self, path: str = None) -> str:
        if path is None:
            path = os.path.join(tempfile.gettempdir(), "khqr_image.webp")
        self.image.save(path, format="WEBP")
        return path

    def to_bytes(self) -> bytes:
        buffer = io.BytesIO()
        self.image.save(buffer, format="PNG")
        return buffer.getvalue()

    def to_base64(self) -> str:
        return base64.b64encode(self.to_bytes()).decode("utf-8")

    def to_data_uri(self) -> str:
        return f"data:image/png;base64,{self.to_base64()}"
