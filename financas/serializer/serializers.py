from rest_framework import serializers
from financas.models.financas_model import Financas


class FinancasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financas
        fields = "__all__"
