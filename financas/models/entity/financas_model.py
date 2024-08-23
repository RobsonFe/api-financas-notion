from uuid import uuid4
import uuid
from django.db import models


class Financas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    entradas = models.DecimalField(max_digits=10, decimal_places=2)
    saidas = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    notion_page_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Financa'
        verbose_name_plural = 'Financas'
