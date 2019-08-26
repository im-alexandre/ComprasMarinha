import json
import requests
import datetime
from sqlalchemy import create_engine
import pandas as pd
import csv
import itertools


#Create database Conection
engine = create_engine('sqlite:///documents.db')

#Load File with USAG Codes
cod_UASG_list = []
with open('codigo UASG.txt', 'r') as csvfile:
    text = csv.reader(csvfile, delimiter=';')
    for row in text:
        cod_UASG_list.append(row[0])

#Creates date range list
data_inicial = datetime.datetime(2018, 1, 1)
data_final = datetime.datetime(2018, 12, 31)

#Create data range
days_list = []
add_day = datetime.timedelta(days=+1)

d_current = data_inicial
d_max = data_final

while d_current <= d_max:
    days_list.append(d_current)
    d_current = d_current + add_day

#Create URL STRING
documents_api = \
    'http://www.transparencia.gov.br/api-de-dados/despesas/documentos?' \
    'unidadeGestora={codUSAG}&dataEmissao={day}%2F{month}%2F{year}&fase={fase}&pagina={page}'

#Create Function to request data from API
def get_documents(codUSAG, document_date, fase, page):
    """

    """
    year = document_date.year
    month = str(document_date.month).zfill(2)
    day = str(document_date.day).zfill(2)
    retorno = 0
    #format url
    url = documents_api.format(codUSAG = codUSAG,day = day,month = month,year = year,fase = fase,page = page)

    #get Response
    response = requests.get(url)
    if response.status_code == 200:
        documents_json = json.loads(response.content)
        retorno = len(documents_json)

        if retorno >0:
            # Save results to database
            documents_df = pd.DataFrame(documents_json)
            documents_df['cod_UASG'] = codUSAG
            documents_df.to_sql('documents', con=engine, if_exists='append')

            get_documents(codUSAG = codUSAG, document_date = document_date, fase = fase,page =  page+1)

    return print( retorno, ' inseridos. Data: ', document_date, 'USAG: ', codUSAG, 'reponse: ', response.status_code)


fase = '1'
page = 1
for coduasg, date in itertools.product(cod_UASG_list,days_list):
    get_documents(codUSAG= coduasg, document_date= date, fase= fase,page = page)