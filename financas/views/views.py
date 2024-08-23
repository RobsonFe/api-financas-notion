from financas.serializer.dto.serializers import FinancasSerializer
from financas.models.entity.financas_model import Financas
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from dotenv import load_dotenv
import financas
import openpyxl
import requests
import logging
import json
import os

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


# get_data_from_notion()


def get_database_properties():
    url = f"https://api.notion.com/v1/databases/{banco_notion}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        properties = response.json().get("properties", {})
        print(json.dumps(properties, indent=4, ensure_ascii=False))
    else:
        print(f"Erro ao buscar propriedades do banco de dados: {
              response.text}")


get_database_properties()


def save_or_update_in_sheet(notion_data):
    logger.debug(f"Chamando save_or_update_in_sheet com dados: {notion_data}")
    file_path = "./planilhas/Finanças.xlsx"
    sheet_name = "Finanças"

    try:
        # Cria um novo workbook se não existir
        if not os.path.exists(file_path):
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = sheet_name
            worksheet.append(
                ["Nome", "Entradas", "Saídas", "Saldo", "Notion Page ID"]
            )
            workbook.save(file_path)

        # Carrega o workbook existente
        workbook = openpyxl.load_workbook(file_path)
        if sheet_name in workbook.sheetnames:
            worksheet = workbook[sheet_name]
        else:
            worksheet = workbook.create_sheet(title=sheet_name)
            worksheet.append(
                ["Nome", "Entradas", "Saídas", "Saldo", "Notion Page ID"]
            )

        # Atualiza ou adiciona a linha na planilha
        id_exists = False
        for row in worksheet.iter_rows(min_row=2, values_only=False):
            if row[4].value == notion_data["notion_page_id"]:
                row[0].value = notion_data["nome"]
                row[1].value = notion_data["entradas"]
                row[2].value = notion_data["saidas"]
                row[3].value = notion_data["saldo"]
                id_exists = True
                break

        if not id_exists:
            worksheet.append([
                notion_data["nome"],
                notion_data["entradas"],
                notion_data["saidas"],
                notion_data["saldo"],
                notion_data["notion_page_id"]
            ])

        workbook.save(file_path)
        logger.info(f"Planilha atualizada e salva em: {file_path}")

    except Exception as e:
        logger.error(f"Erro ao atualizar ou salvar a planilha: {e}")
        raise


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
    serializer_class = FinancasSerializer

    def get_fields(self):
        fields = [field.name for field in Financas._meta.get_fields()]
        fields.remove('notion_page_id')
        return fields

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            url = "https://api.notion.com/v1/pages"
            payload = {
                "parent": {"database_id": banco_notion},
                "properties": {
                    "umtC": {  # ID para "Entradas"
                        "number": data.get("entradas", 0)
                    },
                    "wFRQ": {  # ID para "Saídas "
                        "number": data.get("saidas", 0)
                    },
                    "~Pfs": {  # ID para "Saldo"
                        "number": data.get("saldo", 0)
                    },
                    "title": {  # ID para "Nome"
                        "title": [
                            {"text": {"content": data.get("nome", "")}}
                        ]
                    }
                }
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code in [200, 201]:
                # Salvar a tarefa no banco de dados
                notion_id = response.json()["id"]
                notion = Financas.objects.create(
                    nome=data["nome"],
                    entradas=data["entradas"],
                    saidas=data["saidas"],
                    saldo=data["saldo"],
                    notion_page_id=notion_id
                )

                # Serializar os dados do objeto criado para retorno das respostas
                serializer = self.get_serializer(notion)
                serialized_notion = serializer.data

                # Atualizar a planilha
                notion_data = {
                    "notion_page_id": notion_id,
                    "nome": data["nome"],
                    "entradas": data["entradas"],
                    "saidas": data["saidas"],
                    "saldo": data["saldo"],
                }
                save_or_update_in_sheet(notion_data)

                # Registrar os dados no log em formato JSON
                logger.info(json.dumps(serialized_notion,
                            indent=4, ensure_ascii=False))

                # Retornar os dados criados na resposta
                return Response({"message": "Finança criada com sucesso", "data": serialized_notion}, status=status.HTTP_201_CREATED)

            else:
                # Se a resposta do Notion não for 200 ou 201, trate o erro
                logger.error(
                    "Erro ao criar página no Notion: %s", response.text)
                return Response({"message": "Erro ao criar finança no Notion"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as erro:
            logger.error("Erro ao criar Notion: %s", erro)
            return Response({"message": "Erro ao criar finança"}, status=status.HTTP_400_BAD_REQUEST)


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
