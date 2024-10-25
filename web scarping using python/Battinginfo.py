import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import links
# this code for match information'
all_data=[]
m=""
match_id=links.match_id
for i,mid in zip(links.links,links.match_id): 
 request=requests.get(i)
 m=mid
 sp=BeautifulSoup(request.text,'lxml')
 h_info=sp.find('div',)
 if h_info:
     head=h_info.find('h1')
     ans=head.text.split(',')
     teams=ans[0].split("vs")
     
 table = sp.find_all('table',class_="ds-w-full ds-table ds-table-md ds-table-auto ci-scorecard-table")
 h=0
 for k in table:
  tb = k.find("tbody").find_all('tr')
  g=1
  for row in tb:
     columns = row.find_all('td')
     if len(columns) < 8:  
         continue
     try:
         player_name = row.find('a').get_text(strip=True)
         TeamInnings=teams[h]
         batting_postion=g
         g+=1
         dismissal = columns[1].get_text(strip=True)
         score = columns[2].get_text(strip=True)
         balls_faced = columns[3].get_text(strip=True)
         fours = columns[5].get_text(strip=True)
         six = columns[6].get_text(strip=True)
         strike_rate = columns[7].get_text(strip=True)
         all_data.append({
            "match":ans[0],
            "Batsman Name":player_name,
            "team innings":TeamInnings,
            "batting position":batting_postion,
            "dismissal":dismissal,
            "score":score,
            "ball faced":balls_faced,
            "fours":fours,
            "six":six,
            "strike_rate":strike_rate,
            "match_id":m
         })
     except Exception as e:
         print(f"Error processing row: {e}")
  h=h+1       
 
json_file = 'Batting_summary.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, indent=4, ensure_ascii=False)

header=["match",
            "Batsman Name",
            "team innings",
            "batting position",
            "dismissal",
            "score",
            "ball faced",
            "fours",
            "six",
            "strike_rate",
            "match_id"]
df = pd.DataFrame(all_data, columns=header)
excel_file = 'batting_info.xlsx'
df.to_excel(excel_file, index=False)
print("Data successfully saved to Excel.")


print("Data successfully saved to JSON.")