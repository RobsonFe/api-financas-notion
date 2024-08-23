from rest_framework import generics
from dotenv import load_dotenv
import openpyxl
import requests
import logging
import json
import os

from financas.models.entity.financas_model import Financas
from financas.serializer.dto.serializers import FinancasSerializer

load_dotenv()

# Defina o nível de logging como INFO ou DEBUG
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

notion_token = os.getenv("NOTION_TOKEN")
headers = {
    'Authorization': f"Bearer {notion_token}",
    'Content-Type': 'application/json',
    'Notion-Version': '2022-02-22'
}
banco_notion = os.getenv("ID_DO_BANCO")

if not notion_token or not banco_notion:
    raise ValueError(
        "Token de acesso ao Notion ou ID do banco não encontrado no arquivo .env"
    )

# Buscar dados no Notion


def get_data_from_notion():
    search_params = {"filter": {"value": "page", "property": "object"}}
    search_response = requests.post(
        f'https://api.notion.com/v1/search',
        json=search_params, headers=headers)
    data = json.dumps(search_response.json(), indent=4, ensure_ascii=False)
    print(data)


def delete_from_notion(notion_page_id):
    url = f"https://api.notion.com/v1/pages/{notion_page_id}"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    data = {
        "archived": True
    }
    response = requests.patch(url, json=data, headers=headers)
    if response.status_code != 200:
        logger.error("Erro ao excluir a página no Notion: %s", response.text)
        raise Exception("Erro ao excluir a página no Notion")
    logger.info(
        "Página com Notion Page ID %s arquivada no Notion.", notion_page_id)


class FinancasCreateView(generics.CreateAPIView):
    queryset = Financas.objects.all()
    serializer_class = FinancasSerializer

    def get_fields(self):
        fields = [field.name for field in Financas._meta.get_fields()]
        fields.remove('notion_page_id')
        return fields


class FinancasUpdateView(generics.UpdateAPIView):
    queryset = Financas.objects.all()
    serializer_class = FinancasSerializer


class FinancasListView(generics.ListAPIView):
    queryset = Financas.objects.all()
    serializer_class = FinancasSerializer


class FinancasFindByIdView(generics.RetrieveAPIView):
    queryset = Financas.objects.all()
    serializer_class = FinancasSerializer
    lookup_field = 'pk'


class FinancasFindyByNotionIdView(generics.RetrieveAPIView):
    queryset = Financas.objects.all()
    serializer_class = FinancasSerializer
    lookup_field = 'notion_page_id'


class FinancasDeleteView(generics.DestroyAPIView):
    queryset = Financas.objects.all()
    serializer_class = FinancasSerializer
