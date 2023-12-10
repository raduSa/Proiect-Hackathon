import requests
from bs4 import BeautifulSoup

url = 'https://www.istoric-preturi.info/pd/41417057/IP155GR/telefon-mobil-apple-iphone-15-512-gb-5g-green'

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    container_div = soup.find('div', class_='containerChart')

    if container_div:
        script_tag = container_div.find('script')

        if script_tag:
            data = script_tag.string.strip()
        else:
            print('No <script> tag found within the div.')
    else:
        print('No <div> tag with class "containerChart" found on the webpage.')

else:
    print('Failed to retrieve the webpage. Status code:', response.status_code)
print(data)

indexDate = data.find("\"data\"")
indexPret = data.find("\"datasets\"", indexDate + 1)
indexLast = data.find("\"options\"", indexPret + 1)

l = data.find("[", indexDate, indexPret) + 1
r = data.find("]", indexDate, indexPret)
Date = data[l: r]
Preturi = data[r + 1: indexLast]
# creare lista de date dd/mm/yy
ldates = list()
for x in Date.split(","):
    ldates.append(x[1:len(x) - 1])

# creare liste pt fiecare magazin
indexNext = data.find("label", indexPret + 1)

#dictProdus = dict()
while indexNext > 0:
    res = list()
    l = data.find("[", indexNext) + 1
    r = data.find("]", indexNext)
    Pret = data[l: r]
    indexNume1 = data.find(":", indexNext)
    indexNume2 = data.find(",", indexNext)
    Nume = data[indexNume1 + 2: indexNume2 - 1]
    res.append(Nume)
    for i, x in enumerate(Pret.split(",")):
        if x == "null":
            pass
        else:
            index = x.find(".")
            res.append((ldates[i], int(x[1:index]) + 1))

    print(res)
    indexNext = data.find("label", indexNext + 1)

