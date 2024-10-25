import requests
from bs4 import BeautifulSoup
links=[]
match_id=[]
company="https://www.espncricinfo.com"
res=requests.get('https://www.espncricinfo.com/records/tournament/team-match-results/icc-men-s-t20-world-cup-2024-15946')
soap=BeautifulSoup(res.content,'lxml')

results = soap.find('table', class_="ds-w-full ds-table ds-table-xs ds-table-auto ds-w-full ds-overflow-scroll ds-scrollbar-hide")
tb = results.find("tbody").find_all("tr")

for i in tb:
    td=i.find_all('td')
    a=td[6].find('a')
    match=td[6].find('a').find('span').text
    match_id.append(match)
    links.append(company+a.get('href'))
   
