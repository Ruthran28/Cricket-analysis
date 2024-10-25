import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

try:
    url = 'https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2024-15946'   
    response = requests.get(url)
    sp = BeautifulSoup(response.text, "lxml")
    results = sp.find('table', class_="ds-w-full ds-table ds-table-xs ds-table-auto ds-w-full ds-overflow-scroll ds-scrollbar-hide")
    tb = results.find("tbody").find_all("tr")
    alldata = []
    for tr in tb:
        spa = tr.find_all("td")
        data = [span.get_text() for span in spa]
        alldata.append({
            "Team 1": data[0],
            "Team 2": data[1],
            "Winner": data[2],
            "Won By": data[3],
            "Stadium": data[4],
            "Date": data[5],
            "match_id": data[6]
        })
    
    headers = ['Team 1', 'Team 2', 'Winner', 'Won By', 'Stadium', 'Date', 'match_id']

    df = pd.DataFrame(alldata, columns=headers)
    
  
    excel_file = 'match_info.xlsx'
    df.to_excel(excel_file, index=False)
    print("Data successfully saved to Excel.")
    
    json_file = 'match_info.json'
    with open(json_file, 'w') as f:
        json.dump(alldata, f, indent=4)
    print("Data successfully saved to JSON.")
    
except Exception as e:
    print("An error occurred:", e)
