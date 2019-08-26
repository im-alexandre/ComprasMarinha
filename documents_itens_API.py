import pandas as pd
import json
import requests
from sqlalchemy import create_engine

#Create database Conection
engine = create_engine('sqlite:///documents.db')

#Defines Documents Itens API URL
document_itens_url = 'http://www.transparencia.gov.br/api-de-dados/despesas/subitens-de-empenho?codigoDocumento={documentID}'

#Get documents ID
sql_query = 'select documento from documents'
documents_df = pd.read_sql_query(sql=sql_query,con=engine)

def get_documentsItens(documentID):
    url = document_itens_url.format(documentID=documentID)
    retorno = 0

    response = requests.get(url)
    if response.status_code == 200:
        itens_json = json.loads(response.content)
        retorno = len(itens_json)

        if retorno > 0:
            # Save results to database
            itens_df = pd.DataFrame(itens_json)
            itens_df['documento'] = documentID
            itens_df.to_sql('itens', con=engine, if_exists='append')

    return print(retorno, ' itens inseridos.',  ' reponse: ', response.status_code)

counter = 0
for documento in documents_df['documento']:
    get_documentsItens(documento)
    counter = counter+1
    print(counter)