import os
import zipfile
import qrcode
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.core.management.base import BaseCommand
from QRcode.models import DemoUser

class Command(BaseCommand):
    help = 'Generate QR codes for all DemoUser entries and compress them into a ZIP file.'

    def handle(self, *args, **kwargs):
        try:
            # Paths for storing QR codes and the final ZIP file
            qr_output_dir = os.path.join(settings.BASE_DIR, 'qr_codes')
            zip_output_path = os.path.join(settings.BASE_DIR, 'demo_users_qr.zip')

            # Create the directory if it doesn't exist
            os.makedirs(qr_output_dir, exist_ok=True)

            # Remove any pre-existing ZIP file
            if os.path.exists(zip_output_path):
                os.remove(zip_output_path)

            # Generate QR codes for each DemoUser
            for user in DemoUser.objects.all():
                # Generate QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=1,
                )
                qr.add_data(user.unique_code)
                qr.make(fit=True)

                # Create an image for the QR code
                qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
                draw = ImageDraw.Draw(qr_img)

                # Add user ID below the QR code
                font_path = os.path.join(settings.BASE_DIR, 'Oxanium-Bold.ttf')  # Ensure this font file exists
                font = ImageFont.truetype(font_path, 17)
                text = f"COC<{user.id}>"
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                img_width, img_height = qr_img.size
                new_height = img_height + text_height + 14
                new_img = Image.new('RGB', (img_width, new_height), 'white')
                new_img.paste(qr_img, (0, 0))
                draw = ImageDraw.Draw(new_img)
                draw.text(((img_width - text_width) // 2, img_height + 5), text, fill="black", font=font)

                # Save the image
                qr_file_path = os.path.join(qr_output_dir, f"{user.id}_qr.png")
                new_img.save(qr_file_path)

            # Create a ZIP file containing all QR codes
            with zipfile.ZipFile(zip_output_path, 'w') as zip_file:
                for root, _, files in os.walk(qr_output_dir):
                    for file in files:
                        zip_file.write(
                            os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file), qr_output_dir)
                        )

            # Provide success message
            self.stdout.write(self.style.SUCCESS(f"QR codes generated and zipped successfully: {zip_output_path}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
