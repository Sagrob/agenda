from django.contrib import admin
from core.models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento', 'data_criacao')
    search_fields = ('titulo', 'descricao')