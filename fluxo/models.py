from django.db import models


class Transacao(models.Model):
    TIPO_CHOICES = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]
    
    codigo = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.tipo} - {self.item} (R$ {self.valor})"

class Investimento(models.Model):
    TIPO_INVESTIMENTO = [
        ('ATIVO', 'Investimento Ativo'),
        ('PASSIVO', 'Investimento Passivo'),
    ]
    
    codigo = models.AutoField(primary_key=True)
    item = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=7, choices=TIPO_INVESTIMENTO)

    def __str__(self):
        return f"{self.tipo} - {self.item} (R$ {self.valor})"

