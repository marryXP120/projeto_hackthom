from django.contrib import admin

from .models import Medicao


@admin.register(Medicao)
class MedicaoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "sistolica", "diastolica", "pulso", "data_hora")
    list_filter = ("usuario",)
