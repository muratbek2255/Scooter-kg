import secrets

import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.scooter.models import Scooter


@receiver(post_save, sender=Scooter)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(f'http://localhost:8000/api/v1/scooters/{instance.id}')
        qr.make(fit=True)
        qrcode_img = qr.make_image(fill='black', back_color='white')
        canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qrcode-{instance.address}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        instance.qr_code.save(fname, File(buffer))
        canvas.close()


@receiver(post_save, sender=Scooter)
def generate_promo_code(sender, instance, created, **kwargs):
    if created:
        id_str = str(instance.id)
        upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ1234567890"
        random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
        promo_code = (id_str + random_str)
        instance.code = promo_code
        instance.save()
