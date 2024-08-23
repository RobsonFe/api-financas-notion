# Relatório de Finanças

## Descrição do Projeto

Esse projeto consiste em uma API feita em Django Rest Framework integrada com o banco de dados PostgreSQL e API do Notion, para o gerenciamento de finanças, gerando relatórios em excel a cada requisição, com documentação no Swagger e OpenAPI.

## Tecnologias Utilizadas no Projeto

- Django Rest Framework para o desenvolvimento de aplicações em Python.
- API do Notion para o gerenciamento de tarefas.
- Banco de dados PostgreSQL.
- Swagger e OpenAPI para documentação da API.
- Biblioteca openpyxl para gerar relatórios Python em Excel.

## **Instalação**

- inicie Ambiente Virtual `venv`

```bash
python -m venv venv
```

**Ative o ambiente virtual**:

- No Windows (cmd.exe):

  ```sh
  venv\Scripts\activate.bat
  ```

- No Windows (PowerShell):

  ```sh
  venv\Scripts\Activate.ps1
  ```

- No Git Bash ou Linux/Mac:

  ```sh
  source venv/Scripts/activate
  ```

Para instalar todas as ferramentas necessárias, basta utilizar o `requirements.txt`.

```python
pip install -r requirements.txt
```

## Deixei um `.env` para você configurar suas variáveis de ambiente.

- Instale a Biblioteca

```bash
pip install python-dotenv
```

**Exemplo de como deve ficar o `.env`, precisa apenas colocar o seu caminho.**

```json
SENHA_DO_BANCO_DE_DADOS= ' admin'
```

O nome do arquivo

```vscode
.env
```

## Endpoints da API

### **Link da Documentação da API**

<br>

- [Documentação da API](http://127.0.0.1:8000/docs/)

<br>

- [Documentação da API Alternativa](http://127.0.0.1:8000/redoc/)

<br>

---

- Schema

```json
{
  "nome": "Nome da Finança",
  "entradas": 1234.56,
  "saidas": 789.01,
  "saldo": 445.55,
  "notion_page_id": "71be482c-7403-4b84-a346-22d0fb105b52"
}
```

# Documentação da API

## Visão Geral

Esta API REST gerencia relatórios de finanças com os seguintes campos: `nome`, `entradas`, `saidas`, e `notion_page_id`. Abaixo estão descritos os principais endpoints da API.

## Endpoints

### 1. **Criar Tarefa**

- **URL:** `/api/v1/financas/create/`
- **Método:** `POST`
- **Descrição:** Cria uma nova Finança.
- **Corpo da Requisição:**
  ```json
  {
    "nome": "Nome da Finança",
    "entradas": 1234.56,
    "saidas": 789.01,
    "saldo": 445.55
  }
  ```
- **Resposta de Sucesso:**
  - **Código:** `201 Created`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "_id": "unique_task_id",
      "nome": "Nome da Finança",
      "entradas": 1234.56,
      "saidas": 789.01,
      "saldo": 445.55,
      "notion_page_id": "generated_notion_page_id",
      "__v": 0
    }
    ```
- **Respostas de Erro Comuns:**
  - **Código:** `400 Bad Request` – Se houver erro de validação nos dados.

### 2. **Listar Finanças**

- **URL:** `/api/v1/financas/list`
- **Método:** `GET`
- **Descrição:** Retorna uma lista de todas as Finanças.
- **Parâmetros de Consulta (Opcional):**
  - `page`: Número da página para paginação (padrão: 1).
  - `limit`: Número de resultados por página (padrão: 5).
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "count": 3,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": "427bb9d8-3a7c-44f1-8ae9-e14938742e62",
          "nome": "Nome da Finança Atualizado",
          "entradas": "1234.56",
          "saidas": "789.01",
          "saldo": "445.55",
          "notion_page_id": "71be482c-7403-4b84-a346-22d0fb105b52"
        },
        {
          "id": "d1901855-d565-409f-9e61-91db665263ff",
          "nome": "Nome da Finança",
          "entradas": "1234.56",
          "saidas": "789.01",
          "saldo": "445.55",
          "notion_page_id": "71be482c-7403-4b84-a346-22d0fb105b52"
        },
        {
          "id": "7c5a59c5-eb19-42bb-9fb0-e5459da7edcd",
          "nome": "Nome da Finança 2",
          "entradas": "1234.56",
          "saidas": "789.01",
          "saldo": "445.55",
          "notion_page_id": "71be482c-7403-4b84-a346-22d0fb105b52"
        }
      ]
    }
    ```

### 3. **Obter Detalhes de uma Finança**

- **URL:** `/api/v1/financas/findby/{id}`
- **Método:** `GET`
- **Descrição:** Retorna os detalhes de uma finança específica.
- **Parâmetros de Caminho:**
  - `id`: O ID da tarefa a ser retornada.
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "id": "7c5a59c5-eb19-42bb-9fb0-e5459da7edcd",
      "nome": "Nome da Finança 2",
      "entradas": "1234.56",
      "saidas": "789.01",
      "saldo": "445.55",
      "notion_page_id": "71be482c-7403-4b84-a346-22d0fb105b52"
    }
    ```
- **Respostas de Erro Comuns:**
  - **Código:** `404 Not Found` – Se a finança com o ID fornecido não for encontrada.

### 4. **Atualizar Finança**

- **URL:** `/api/v1/financas/update/{id}`
- **Método:** `PUT`
- **Descrição:** Atualiza uma finança existente.
- **Parâmetros de Caminho:**
  - `id`: O ID da finança a ser atualizada.
- **Corpo da Requisição:**
  ```json
  {
    "id": "7c5a59c5-eb19-42bb-9fb0-e5459da7edcd",
    "nome": "Nome da Finança",
    "entradas": "1234.56",
    "saidas": "789.01",
    "saldo": "445.55",
    "notion_page_id": "71be482c-7403-4b84-a346-22d0fb105b52"
  }
  ```
- **Resposta de Sucesso:**
  - **Código:** `200 OK`
  - **Exemplo de Corpo da Resposta:**
    ```json
    {
      "id": "7c5a59c5-eb19-42bb-9fb0-e5459da7edcd",
      "nome": "Nome da Finança Atualizada",
      "entradas": "1234.56",
      "saidas": "789.01",
      "saldo": "445.55",
      "notion_page_id": "71be482c-7403-4b84-a346-22d0fb105b52"
      "updatedAt": "2024-08-20T14:00:00Z",
      "__v": 0
    }
    ```
- **Respostas de Erro Comuns:**
  - **Código:** `400 Bad Request` – Se houver erro de validação nos dados.
  - **Código:** `404 Not Found` – Se a tarefa com o ID fornecido não for encontrada.

### 5. **Deletar Tarefa**

- **URL:** `/api/v1/financas/delete/{id}`
- **Método:** `DELETE`
- **Descrição:** Remove uma finança específica.
- **Parâmetros de Caminho:**
  - `id`: O ID da finança a ser removida.
- **Resposta de Sucesso:**
  - **Código:** `204 No Content`
- **Respostas de Erro Comuns:**
  - **Código:** `404 Not Found` – Se a finança com o ID fornecido não for encontrada.

## License

Licença [MIT licensed](LICENSE).
