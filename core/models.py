from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Evento(models.Model):
    titulo = models.CharField(max_length=100, default="Titulo")
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(null=True, verbose_name='Data do evento')
    data_criacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'eventos'


    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y - %H:%M')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False
