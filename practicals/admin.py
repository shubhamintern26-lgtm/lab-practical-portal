from django.contrib import admin
from .models import Subject, Practical


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at")
    search_fields = ("name", "code")


@admin.register(Practical)
class PracticalAdmin(admin.ModelAdmin):
    list_display = ("practical_number", "title", "subject", "created_at")
    list_filter = ("subject",)
    search_fields = ("title", "subject__name")
    ordering = ("subject", "practical_number")