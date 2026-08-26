from django.contrib import admin
from django.utils.html import format_html

from .models import Subject, Practical


# =========================================================
# SUBJECT ADMIN
# =========================================================

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "qr_preview",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
    )

    readonly_fields = (
        "qr_preview",
    )

    list_per_page = 20

    def qr_preview(self, obj):

        if obj.qr_code:
            return format_html(
                '<img src="{}" '
                'width="180" '
                'height="180" '
                'style="object-fit:contain; '
                'border:1px solid #ddd; '
                'border-radius:8px; '
                'padding:5px; '
                'background:white;" />',
                obj.qr_code.url
            )

        return format_html(
            '<span style="color:#999;">QR not generated</span>'
        )

    qr_preview.short_description = "QR Code"


# =========================================================
# PRACTICAL ADMIN
# =========================================================

@admin.register(Practical)
class PracticalAdmin(admin.ModelAdmin):

    list_display = (
        "practical_number",
        "title",
        "subject",
        "created_at",
    )

    list_filter = (
        "subject",
    )

    search_fields = (
        "title",
        "subject__name",
        "subject__code",
    )

    ordering = (
        "subject",
        "practical_number",
    )

    list_per_page = 20