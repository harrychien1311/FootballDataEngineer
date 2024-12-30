import lxml
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
import pandas as pd
import json

def get_info(url: str):
    source = requests.get(url).text
    page = BeautifulSoup(source, "lxml")
    tab = page.find_all("a", class_="Standing_standings__rowGrid__45OOd")
    return tab

def extract_and_transform_data(url, ti):
    table = []
    tab = get_info(url)
    for i in range(len(tab)):
        #table.append(tab[i].text.strip())
        info = tab[i].find_all('div')
        value = {}
        value['rank'] = i+1
        if len(info) == 10:
            value.update({
                "team": info[3].text,
                "no_match": int(info[4].text),
                "points": int(info[9].text)    
            })
        else:
            value.update({
                "team": info[2].text,
                "no_match": int(info[3].text),
                "points": int(info[8].text)  
            })
        table.append(value)
        json_rows = json.dumps(table)
        ti.xcom_push(key='epl_standings', value=json_rows)

def save_to_db(ti):
    standings = ti.xcom_pull(key='epl_standings', task_ids = 'extract_and_transform')
    data = json.loads(standings)
    data = pd.DataFrame(data)

    engine = create_engine(f'postgresql+psycopg2://postgres:postgres@172.21.69.190:54320/postgres')
    data.to_sql('epl_standings', engine, if_exists='replace', index=False)


