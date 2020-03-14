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


