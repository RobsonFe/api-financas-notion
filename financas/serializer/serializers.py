from rest_framework import serializers
from financas.models.financas_model import Financas


class FinancasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financas
        fields = "__all__"
        
class FinancasCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financas
        fields = ("nome", "entradas", "saidas", "saldo")

    def create(self, validated_data):
        # Calcula o saldo automaticamente
        saldo = validated_data.get("entradas", 0) - validated_data.get("saidas", 0)
        validated_data["saldo"] = saldo  # Adiciona o saldo ao validated_data
        return super().create(validated_data)
class FinancasUpdateSerializer(serializers.ModelSerializer):
    saldo = serializers.SerializerMethodField()

    class Meta:
        model = Financas
        fields = "nome", "entradas", "saidas", "saldo"

    def get_saldo(self, obj):
        return obj.entradas - obj.saidas

    def update(self, instance, validated_data):
        instance.nome = validated_data.get('nome', instance.nome)
        instance.entradas = validated_data.get('entradas', instance.entradas)
        instance.saidas = validated_data.get('saidas', instance.saidas)
        instance.saldo = instance.entradas - instance.saidas
        instance.save()
        return instance