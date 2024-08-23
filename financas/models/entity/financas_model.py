from uuid import uuid4
import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Financas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    entradas = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    saidas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notion_page_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Finança'
        verbose_name_plural = 'Finanças'
        indexes = [
            models.Index(fields=['nome']),
        ]

    def save(self, *args, **kwargs):
        # Atualiza o saldo com base nas entradas e saídas
        self.saldo = self.entradas - self.saidas
        # Valida que o saldo não é negativo
        if self.saldo < 0:
            raise ValidationError("O saldo não pode ser negativo.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
