from tabulate import tabulate
import openpyxl
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_sheet(notion_data):
    
    logger.debug(f"Chamando save_or_update_in_sheet com dados: {notion_data}")
    file_path = "./planilhas/Finanças.xlsx"
    sheet_name = "Finanças"
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    try:
        if not os.path.exists(file_path):
            worksheet.title = sheet_name
            worksheet.append(
                [
                    "Nome", 
                    "Entradas", 
                    "Saídas",
                    "Saldo", 
                    "Notion Page ID"
                ]
                )
            workbook.save(file_path)
            workbook = openpyxl.load_workbook(file_path)
            logger.debug(f"Planilha criada com sucesso em: {file_path}")

        if sheet_name in workbook.sheetnames:
            worksheet = workbook[sheet_name]
        else:
            worksheet = workbook.create_sheet(title=sheet_name)
            worksheet.append(
                [
                    "Nome", 
                    "Entradas", 
                    "Saídas",
                    "Saldo", 
                    "Notion Page ID"
                ]
                )

    except Exception as e:
        logger.error(f"Erro ao salvar a planilha: {e}")
        raise
    

def update_sheet(notion_data):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        try:
            logger.debug(f"Atualizando dados: {notion_data}")
            file_path = "./planilhas/Finanças.xlsx"
        
            logger.debug("Iniciando verificação de existência do Notion Page ID na planilha")
            
            id_exists = False
            updated_row = []
            
            for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, values_only=False):
                
                notion_id = row[4].value
                
                if notion_id == notion_data["notion_page_id"]:
                    
                    row[0].value = notion_data["nome"]
                    row[1].value = notion_data["entradas"]
                    row[2].value = notion_data["saidas"]
                    row[3].value = notion_data["saldo"]
                    
                    id_exists = True
                    
                    updated_row = [
                        notion_data["nome"], 
                        notion_data["entradas"],
                        notion_data["saidas"], 
                        notion_data["saldo"], 
                        notion_data["notion_page_id"]
                        ]
                    
                    break

            if not id_exists:
                logger.debug("ID não encontrado, adicionando nova linha")
                worksheet.append([
                    notion_data["nome"],
                    notion_data["entradas"],
                    notion_data["saidas"],
                    notion_data["saldo"],
                    notion_data["notion_page_id"]
                ])
                updated_row = [
                    notion_data["nome"], 
                    notion_data["entradas"],
                    notion_data["saidas"], 
                    notion_data["saldo"], 
                    notion_data["notion_page_id"]
                    ]

            workbook.save(file_path)
            logger.info(f"Planilha atualizada e salva em: {file_path}")

            # Log do conteúdo atualizado da linha
            logger.info("Conteúdo da linha atualizada:")
            table_headers = ["Nome", "Entradas","Saídas", "Saldo", "Notion Page ID"]
            logger.info(tabulate([updated_row], headers=table_headers, tablefmt="grid"))
            
        except Exception as e:
            logger.error(f"Erro ao atualizar planilha: {e}")
            raise

def delete_sheet(notion_page_id):
    
    logger.debug(f"Chamando delete_sheet com Notion Page ID: {notion_page_id}")
    file_path = "./planilhas/Finanças.xlsx"
    sheet_name = "Finanças"

    if not os.path.exists(file_path):
        logger.warning("O arquivo de planilha não foi encontrado.")
        return

    workbook = openpyxl.load_workbook(file_path)

    if sheet_name not in workbook.sheetnames:
        logger.warning("A planilha '%s' não existe no arquivo.", sheet_name)
        return

    worksheet = workbook[sheet_name]

    # Encontre e exclua a linha com o Notion Page ID correspondente
    rows_to_delete = []
    
    for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, values_only=False):
        
        if row[4].value == notion_page_id:
            rows_to_delete.append(row[0].row)

    # Excluir as linhas encontradas na ordem inversa
    for row_idx in reversed(rows_to_delete):
        worksheet.delete_rows(row_idx)

    workbook.save(file_path)
    logger.info(f"Linhas com Notion Page ID {notion_page_id} excluídas da planilha.")