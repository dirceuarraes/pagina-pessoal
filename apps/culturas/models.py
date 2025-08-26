from django.db import models

# Create your models here.
class Cultura(models.Model):
    nome = models.CharField(max_length=100)
    kc_inicial = models.FloatField()
    kc_medio = models.FloatField()
    kc_final = models.FloatField()
    z_min = models.FloatField()
    z_max = models.FloatField()
    p = models.FloatField()


    def __str__(self):
        return self.nome