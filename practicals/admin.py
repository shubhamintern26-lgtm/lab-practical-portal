from django.contrib import admin
from django.utils.html import format_html

from .models import Subject, Practical


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "qr_preview",
        "print_qr",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
    )

    readonly_fields = (
        "qr_preview",
    )

    def qr_preview(self, obj=None):

        if obj and obj.pk:
            return format_html(
                '<img src="{}" width="120" height="120" '
                'style="object-fit:contain;'
                'border:1px solid #e2e8f0;'
                'border-radius:8px;padding:5px;'
                'background:white;" />',
                obj.get_qr_code_data(),
            )

        return "QR not generated"

    def print_qr(self, obj):

        if obj and obj.pk:

            url = f"/subject/{obj.pk}/qr-print/"

            return format_html(
                '<a href="{}" target="_blank" '
                'style="background:#2563eb;color:white;'
                'padding:6px 12px;border-radius:6px;'
                'text-decoration:none;font-weight:600;">'
                '🖨 Print QR'
                '</a>',
                url,
            )

        return "-"

    print_qr.short_description = "Print QR"


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
    )

    ordering = (
        "subject",
        "practical_number",
    )