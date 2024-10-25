import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
res=requests.get('https://www.espncricinfo.com/series/icc-men-s-t20-world-cup-2024-1411166/squads')
soap=BeautifulSoup(res.content,"lxml")
alldata=[]
squad=soap.find('div',class_='ds-mb-4')
teams=squad.find_all('a')
for i in teams:
    team_name=i.find('span')
    
    link="https://www.espncricinfo.com"+i.get('href')
    req=requests.get(link)
    sp=BeautifulSoup(req.content,"lxml")
    players_data=sp.find_all('div',class_="ds-grid lg:ds-grid-cols-2")
    for i in players_data:
        for j in i.find_all('div',class_="ds-border-line odd:ds-border-r ds-border-b"):
            k=j.find_all('span')
            Player_name=k[1].get_text()
            team=team_name.text
            player_role=j.find('p').text
            p=j.find('div',class_='ds-justify-between ds-text-typo-mid3')
            g=p.find_all('div',class_='ds-flex ds-items-start ds-space-x-1')
            batting_style="-"
            bowling_style="-"
            if(len(g)==2):
                ba=g[0].find_all('span')
                bo=g[1].find_all('span')
                batting_style=ba[1].text
                bowling_style=bo[1].text
            elif(len(g)==1):
                t=g[0].find_all('span')
                if(t[0].text=="Batting:"):
                    batting_style=t[1].text
                else:
                    bowling_style=t[1].text 
            alldata.append({
                "name":Player_name,"Team":team,"Player Role":player_role,"Batting Style":batting_style,"Bowling Style":bowling_style
            })    
   
json_file="player_submary.json"
with open(json_file, 'w', encoding='utf-8') as f:
 json.dump(alldata, f, indent=4, ensure_ascii=False)
print("Data successfully saved to JSON.")    

excel_file="player_submary.xlsx"
header=["name","Team","Player Role","Batting Style","Bowling Style"]
data=pd.DataFrame(alldata,columns=header)
data.to_excel(excel_file,index=False)
print("data successfully saved in excel")