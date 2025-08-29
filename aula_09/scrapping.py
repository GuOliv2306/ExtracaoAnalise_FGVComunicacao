import requests
from bs4 import BeautifulSoup
import pandas as pd

url='https://www.scrapethissite.com/pages/forms/'

lista_teams=[]
for page in range(1,25):
    response = requests.get(url+f'?page_num={page}').content
    soup= BeautifulSoup(response,'html.parser')

    teams= soup.find_all('tr',class_='team')

    for team in teams:
        nome = team.find('td', class_='name').get_text().strip()
        year=team.find('td',class_='year').get_text().strip()
        Wins=team.find('td',class_='wins').get_text().strip()
        Losses=team.find('td',class_='losses').get_text().strip()
        Ot_Losses=team.find('td',class_='ot-losses').get_text().strip()
        Pct_wins=team.find('td',class_=['pct', 'text-success']).get_text().strip()
        Gf=team.find('td',class_='gf').get_text().strip()
        Ga=team.find('td',class_='ga').get_text().strip()
        Dif_success= team.find('td', class_=['diff', 'text-success']).get_text().strip()
        
        def pct_wins():
            valor=float(Pct_wins)*100
            return f'{valor:.2f}%'

        dados={'nome':nome,'year':year,'Wins':Wins,'Losses':Losses,'Pct_wins':pct_wins(),'Ot_Losses':Ot_Losses,'Gf':Gf,'Ga':Ga,'Dif_success':float(Dif_success)}

        lista_teams.append(dados)

df=pd.DataFrame(lista_teams)

print(df)

df.to_csv('C:\\Users\\guguo\\OneDrive\\Área de Trabalho\\FGV\\extracao_dados\\ExtracaoAnalise_FGVComunicacao\\bases\\nhl_teams.csv',index=False,encoding='utf-8')

