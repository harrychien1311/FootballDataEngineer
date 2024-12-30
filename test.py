import lxml
import requests
from bs4 import BeautifulSoup
import re
import time
from pprint import pprint



link = f"https://onefootball.com/en/competition/premier-league-9/table"
source = requests.get(link).text
page = BeautifulSoup(source, "lxml")
tab = page.find_all("a", class_="Standing_standings__rowGrid__45OOd")
# tab_rows = tab.find("div")
table = []
#table.append("  ________________ PL W D L GD PTS")



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


pprint(table)