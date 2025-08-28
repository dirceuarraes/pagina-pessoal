from django.db import models
from django.utils import timezone

class Solo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Solo")
    descricao = models.TextField(verbose_name="Descrição")
    capacidade_campo = models.FloatField(verbose_name="Capacidade de Campo (%)")
    ponto_murcha = models.FloatField(verbose_name="Ponto de Murcha Permanente (%)")
    densidade = models.FloatField(verbose_name="Densidade do Solo (g/cm³)")
    condutividade_hidraulica = models.FloatField(verbose_name="Condutividade Hidráulica (cm/h)")
    data_cadastro = models.DateTimeField("Data de Cadastro", default=timezone.now)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Solo"
        verbose_name_plural = "Solos"