from django.db import models

# Create your models here.
class Solo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    capacidade_campo = models.FloatField()
    ponto_murcha = models.FloatField() 
    densidade = models.FloatField()
    condutividade_hidraulica = models.FloatField()  

    def __str__(self):
        return self.nome