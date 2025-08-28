from django.db import models

# Create your models here.
class Cultura(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Cultura")
    kc_inicial = models.FloatField(verbose_name="Kc Inicial")
    kc_medio = models.FloatField(verbose_name="Kc Médio")
    kc_final = models.FloatField(verbose_name="Kc Final")
    z_min = models.FloatField(verbose_name="Z Min (m)")
    z_max = models.FloatField(verbose_name="Z Max (m)")
    p = models.FloatField(verbose_name="Fator de depleção (-)")


    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cultura"
        verbose_name_plural = "Culturas"
        ordering = ['nome']