from django.db import models
from django.conf import settings
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files import File


class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    qr_code = models.ImageField(
        upload_to="qrcodes/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse(
            "subject_detail",
            kwargs={"subject_id": self.id}
        )

    def save(self, *args, **kwargs):

        # Pehle Subject save karo,
        # taaki usko ID mil jaye.
        super().save(*args, **kwargs)

        # QR URL
        qr_url = f"{settings.SITE_URL}{self.get_absolute_url()}"

        # QR generate
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(qr_url)
        qr.make(fit=True)

        qr_image = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        # Image ko memory me save karo
        buffer = BytesIO()

        qr_image.save(
            buffer,
            format="PNG"
        )

        file_name = f"{self.code}_qr.png"

        # Django ImageField me save
        self.qr_code.save(
            file_name,
            File(buffer),
            save=False
        )

        # QR ke saath object update
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