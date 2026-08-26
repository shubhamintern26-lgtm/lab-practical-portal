from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Practical(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="practicals"
    )
    practical_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    aim = models.TextField()
    requirements = models.TextField(blank=True)
    theory = models.TextField(blank=True)
    procedure = models.TextField(blank=True)
    code = models.TextField(blank=True)
    output_image = models.ImageField(
        upload_to="practical_outputs/",
        blank=True,
        null=True
    )
    viva_questions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["practical_number"]
        unique_together = ["subject", "practical_number"]

    def __str__(self):
        return f"{self.subject.name} - Practical {self.practical_number}"