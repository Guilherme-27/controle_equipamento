from django.contrib import admin
from .models import Ambiente, Equipamento, Status


@admin.register(Ambiente)
class AmbienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")
    search_fields = ("nome",)


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "ambiente", "status", "data_atualizacao")
    list_filter = ("ambiente", "status")
    search_fields = ("nome",)
