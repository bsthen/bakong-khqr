import os
import io
import base64
import qrcode
import tempfile
import qrcode.constants
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from importlib import resources
from .emv_parser import EMVParser

class ImageTools:
    def __init__(self):
        try:
            with resources.files("bakong_khqr.sdk.assets").joinpath("regular.ttf").open("rb") as f:
                self.__regular_font = ImageFont.truetype(f, 13)
                
            with resources.files("bakong_khqr.sdk.assets").joinpath("bold.ttf").open("rb") as f:
                self.__bold_font = ImageFont.truetype(f, 22)
                
            with resources.files("bakong_khqr.sdk.assets").joinpath("logo.png").open("rb") as f:
                self.__khqr_logo = Image.open(f).convert("RGBA")
                
            with resources.files("bakong_khqr.sdk.assets").joinpath("USD.png").open("rb") as f:
                self.__usd_icon = Image.open(f).convert("RGBA")
                
            with resources.files("bakong_khqr.sdk.assets").joinpath("KHR.png").open("rb") as f:
                self.__khr_icon = Image.open(f).convert("RGBA")
                
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Required asset not found: {e.filename}. Please ensure the assets are correctly installed.") from e
        
    def __draw_red_corner(self, draw, width, height, fold_size=40, color="#cc0000"):
    # Top-right triangle (fold)
        triangle = [
            (width - fold_size, 0),       # top edge left of corner
            (width, 0),                   # top-right corner
            (width, fold_size)           # right edge below corner
        ]
        draw.polygon(triangle, fill=color)


    def __add_rounded_corners(self, image, radius):
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
        khqr_logo = self.__khqr_logo.resize((90, 21))
        img.paste(khqr_logo, (width // 2 - 40, 20), khqr_logo)

        # Merchant name, amount, currency with loaded fonts
        draw.text((32, 80), merchant_name, fill="black", font=self.__regular_font)
        # Format amount and measure its width
        amount_text = f"{amount:,.2f}"
        # Use a dummy draw object to measure text
        dummy_img = Image.new("RGB", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)

        # Get bounding box of the amount text
        bbox = dummy_draw.textbbox((0, 0), amount_text, font=self.__bold_font)
        amount_width = bbox[2] - bbox[0]  # right - left

        # Draw amount
        draw.text((30, 110), amount_text, fill="black", font=self.__bold_font)

        # Draw currency next to amount
        currency_x = 30 + amount_width + 5
        draw.text((currency_x, 119), currency, fill="black", font=self.__regular_font)


        # Dashed line
        self.__draw_dashed_line(draw, (0, 150), (340, 150), dash_length=2, gap_length=4, fill="grey", width=1)

        # Paste QR code
        img.paste(qr_img, (10, 160))

        # Currency icon
        currency_icon = self.__usd_icon if currency == "USD" else self.__khr_icon
        currency_icon = currency_icon.resize((40, 40))
        img.paste(currency_icon, (width // 2 - 20, 280), currency_icon)

        # Draw red corner & round corners
        self.__draw_red_corner(draw, width, height, fold_size=90)
        rounded_img = self.__add_rounded_corners(img, radius=15)

        # Return wrapped result
        return QRImageResult(rounded_img)

    
class QRImageResult:
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
