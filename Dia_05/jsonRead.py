import requests
import json
import pandas as pd
import time

# importando os pacotes necessários aos gráficos
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed, interact_manual
import ipywidgets as widget

import pytz #https://www.geeksforgeeks.org/python-pytz/
import datetime
from datetime import datetime
i = 0
ID = [] 
DATA = [] 
HORA = []
TENSAO = []
TEMP = []
BTN = [] 
MOTOR = [] 
ALARME = []
IP = '10.162.104.158'
def JSONfromIP(url = f'{IP}'):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        with open('dados.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 3. Carregar dados do arquivo JSON
        with open('dados.json', 'r', encoding='utf-8') as f:
            dados_carregados = json.load(f)

        # 4. Converter os dados para um DataFrame
        df = pd.DataFrame(dados_carregados)

        # 5. Exibir os dados
        return df
    else:
        print("Erro ao conectar ao servidor ESP32")

def Agora():
    datetime_br= datetime.now(pytz.timezone('America/Sao_Paulo'))
    D_H = 'Data e Hora atual: ' + str(datetime_br.strftime('%d/%m/%Y %H:%M:%S'))
    D = data_atual = datetime_br.strftime('%d/%m/%Y')
    H = hora_atual = datetime_br.strftime('%H:%M:%S')
    return D_H, D, H

'''
for i in range(3600):    
    NOW = Agora()
    ID.append(i)
    DATA.append(NOW[1]) #DATA
    HORA.append(NOW[2]) #HORA
    DF = JSONfromIP('192.168.15.4')
    TENSAO.append(DF['Tensao'][0])
    TEMP.append(DF['Temperatura'][0])
    BTN.append(DF['botao'][0])
    MOTOR.append(DF['motor'][0])
    ALARME.append(DF['alarme'][0])
    i+=1 #incrementa contador índice de registros
    #DB = pd.DataFrame(ID, DATA, HORA, TENSAO, TEMP)
    DB = pd.DataFrame({
    'ID': ID,
    'DATA': DATA,
    'HORA': HORA,
    'TENSAO': TENSAO,
    'TEMPERATURA [ºC]': TEMP,
    'BOTAO': BTN,
    'MOTOR': MOTOR,
    'ALARME': ALARME
    })
    print(DB)

    time.sleep(5) # Sleep for 5 seconds

'''
