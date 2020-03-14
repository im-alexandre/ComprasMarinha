import json
import requests as r
import sqlalchemy as sqla
import pandas as pd
import csv

url = 'http://compras.dados.gov.br/pregoes/v1/pregoes.json'

def get_pregoes(uasg: str):
    data = {'co_uasg': str(uasg)}
    response = r.request('GET', url=url, params=data)
    return response.json()

pd.DataFrame.from_dict(get_pregoes('762200')['_embedded']).to_csv('teste_api.csv')


# df = pd.read_csv('teste_api.csv')
# print(df)