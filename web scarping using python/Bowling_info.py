import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import links
alldata=[]
m=""
for url ,mid in zip(links.links,links.match_id):
  req=requests.get(url)
  m=mid
  soap=BeautifulSoup(req.content,'lxml')
  table = soap.find_all('table',class_="ds-w-full ds-table ds-table-md ds-table-auto")
  h_info=soap.find('div',)
  #match details
  if h_info:
     head=h_info.find('h1')
     ans=head.text.split(',')
     teams=ans[0].split("vs") 
  h=1   
  for k in table:
     tb = k.find("tbody").find_all('tr')
     for row in tb:
        columns = row.find_all('td')
        if len(columns) < 8:  
            continue
        try:
         player_name=row.find('a').get_text(strip=True)
         overs=columns[1].get_text(strip=True)
         mainden=columns[2].get_text(strip=True)
         Runs=columns[3].get_text(strip=True)
         Wicket=columns[4].get_text(strip=True)
         Economy=columns[5].get_text(strip=True)
         zeros=columns[6].get_text(strip=True)
         fours=columns[7].get_text(strip=True)
         sixes=columns[8].get_text(strip=True)
         Wide=columns[9].get_text(strip=True)
         noball=columns[10].get_text(strip=True)
         alldata.append({
             "match":ans[0],
            "bowler Name":player_name,
            "Team":teams[h],
            "Overs":overs,
            "maiden":mainden,
            "Runs":Runs,
            "wicket":Wicket,
            "Economy":Economy,
            "zeros":zeros,
            "fours":fours,
            "Six":sixes,
            "Wide":Wide,
            "Noball":noball,
            "match_id":m
            })
        except Exception as e:
              print(e)
     h-=1   
json_file="Bowling_submary.json"
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(alldata, f, indent=4, ensure_ascii=False)
print("Data successfully saved to JSON.")
header=[ "match",
            "bowler Name",
            "Team",
            "Overs",
            "maiden",
            "Runs",
            "wicket",
            "Economy",
            "zeros",
            "fours",
            "Six",
            "Wide",
            "Noball",
            "match_id"]
data=pd.DataFrame(alldata,columns=header)
excel_file="bowling_info.xlsx"
data.to_excel(excel_file,index=False)
print("data successfully saved in excel")

