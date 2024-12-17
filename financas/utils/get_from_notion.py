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


# Buscar dados do Notion

def get_data_from_notion():
    search_params = {
        "filter": {
                "value": 
                "page", 
                "property": "object"
                }
            }
    search_response = requests.post(f'https://api.notion.com/v1/search',json=search_params, headers=headers)
    data = json.dumps(search_response.json(), indent=4, ensure_ascii=False)
    print(data)


# obter dados das propriedades do Notion

def get_database_properties():
    url = f"https://api.notion.com/v1/databases/{banco_notion}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        properties = response.json().get("properties", {})
        print(json.dumps(properties, indent=4, ensure_ascii=False))
    else:
        print(f"Erro ao buscar propriedades do banco de dados: {
              response.text}")

# Teste de requisição para API do Notion.
if __name__ == "__main__":
    pass
    # get_data_from_notion()
    # get_database_properties()