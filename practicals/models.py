from django.db import models
from django.urls import reverse
from django.core.files import File
from django.conf import settings

import qrcode
from io import BytesIO


class Subject(models.Model):
    name = models.CharField(max_length=200)

    code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    qr_code = models.ImageField(
        upload_to="qrcodes/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse(
            "subject_detail",
            args=[self.id]
        )

    def save(self, *args, **kwargs):

        # First save subject so it gets an ID
        super().save(*args, **kwargs)

        # ==================================================
        # QR CODE URL
        # ==================================================

        site_url = getattr(
            settings,
            "SITE_URL",
            "http://10.74.246.175:8000"
        )

        subject_url = (
            f"{site_url}"
            f"{self.get_absolute_url()}"
        )

        # ==================================================
        # GENERATE QR CODE
        # ==================================================

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(subject_url)
        qr.make(fit=True)

        qr_image = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        # ==================================================
        # SAVE QR IMAGE
        # ==================================================

        buffer = BytesIO()

        qr_image.save(
            buffer,
            format="PNG"
        )

        buffer.seek(0)

        filename = f"{self.code}_QR.png"

        # Delete old QR before creating new one
        if self.qr_code:
            self.qr_code.delete(
                save=False
            )

        self.qr_code.save(
            filename,
            File(buffer),
            save=False
        )

        # Save QR field only
        super().save(
            update_fields=["qr_code"]
        )


class Practical(models.Model):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="practicals"
    )

    practical_number = models.PositiveIntegerField()

    title = models.CharField(
        max_length=200
    )

    aim = models.TextField()

    requirements = models.TextField(
        blank=True
    )

    theory = models.TextField(
        blank=True
    )

    procedure = models.TextField(
        blank=True
    )

    code = models.TextField(
        blank=True
    )

    output_image = models.ImageField(
        upload_to="practical_outputs/",
        blank=True,
        null=True
    )

    viva_questions = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["practical_number"]

        unique_together = [
            "subject",
            "practical_number"
        ]

    def __str__(self):
        return (
            f"{self.subject.name} - "
            f"Practical {self.practical_number}"
        )