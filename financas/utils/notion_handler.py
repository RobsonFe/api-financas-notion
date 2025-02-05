from math import e
from dotenv import load_dotenv
import requests
import logging
import json
import os

load_dotenv()

# Defina o nível de logging como INFO ou DEBUG
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

notion_token = os.getenv("NOTION_TOKEN")
id_banco_financas = os.getenv("BANCO_FINANCAS")

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

data = {
  "nome": "Teste 3 para testar retorno do Notion",
  "entradas": 666.66,
  "saidas": 66.01,
  "saldo": 800.55
}

# Buscar dados do Notion

def get_data_from_notion():
    search_params = {
        "filter": {
                "value": 
                "page", 
                "property": "object"
                }
            }
    response = requests.post(f'https://api.notion.com/v1/search',json=search_params, headers=headers)
    # data = json.dumps(response.json(), indent=4, ensure_ascii=False)
    # data = response.json().get('object', {})
    # data = response.json().get("results", {})[0].get("properties", {})['Entradas']['number']
    # data = response.json().get("results", {})[0].get("properties", {})['Entradas']
    # data = response.json().get("results", {})[0].get("properties", {})
    # data = response.json().get("results", {})[0]
    data = response.json().get("results", {})
    result = json.dumps(data, indent=4, ensure_ascii=False)
    print(result)


def create_data_from_notion(data, *args, **kwargs):
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
        if response.status_code == 200:
         print(f'Dados criados com sucesso {json.dumps(response.json(), indent=4, ensure_ascii=False)}')
        else:
            logger.error(f"Erro ao criar dados: {json.dumps(response.json(), indent=4, ensure_ascii=False)}")

# obter dados das propriedades do Notion

def get_database_properties():
    url = f"https://api.notion.com/v1/databases/{banco_notion}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # properties = response.json().get("properties", {})
        # properties = response.json().get("properties", {}).get("Nome", {}).get("name")
        properties = response.json().get("properties", {}).get("Nome", {}).get("title", {})
        print(json.dumps(properties, indent=4, ensure_ascii=False))
    else:
        print(f"Erro ao buscar propriedades do banco de dados: {response.text}")

# Teste de requisição para API do Notion.
if __name__ == "__main__":
    # create_data_from_notion(data=data)
    get_data_from_notion()
    # get_database_properties()