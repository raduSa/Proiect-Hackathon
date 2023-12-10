import requests
from bs4 import BeautifulSoup

dictMag = dict()
def inputProd(url):

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
    #print(data)

    indexDate = data.find("\"data\"")
    indexPret = data.find("\"datasets\"", indexDate + 1)
    indexLast = data.find("\"options\"", indexPret + 1)

    l = data.find("[", indexDate, indexPret) + 1
    r = data.find("]", indexDate, indexPret)
    Date = data[l: r]
    Preturi = data[r + 1 : indexLast]
    # creare lista de date dd/mm/yy
    ldates = list()
    for x in Date.split(","):
        ldates.append(x[1:len(x) - 1])

    # creare dictionar pt produs
    indexNext = data.find("label", indexPret + 1)

    dictProd = dict()
    while indexNext > 0:
        l = data.find("[", indexNext) + 1
        r = data.find("]", indexNext)
        Pret = data[l: r] #partea din string cu preturile de la magazinul Nume
        indexNume1 = data.find(":", indexNext)
        indexNume2 = data.find(",", indexNext)
        Nume = data[indexNume1 + 2: indexNume2 - 1]#Nume magazin
        dictProd[Nume] = {x + 1 : [] for x in range(12)}
        valid = False

        for i, x in enumerate(Pret.split(",")):
            if x == "null":
                pass
            else:
                index = x.find(".")
                pret = int(x[1:index]) + 1
                luna = ldates[i][3 : 6]
                an = int(ldates[i][7 : 11])
                if int(an) == 2023:
                    valid = True
                    if luna == "Ian":
                        dictProd[Nume][1].append(pret)
                    elif luna == "Feb":
                        dictProd[Nume][2].append(pret)
                    elif luna == "Mar":
                        dictProd[Nume][3].append(pret)
                    elif luna == "Apr":
                        dictProd[Nume][4].append(pret)
                    elif luna == "Mai":
                        dictProd[Nume][5].append(pret)
                    elif luna == "Iun":
                        dictProd[Nume][6].append(pret)
                    elif luna == "Iul":
                        dictProd[Nume][7].append(pret)
                    elif luna == "Aug":
                        dictProd[Nume][8].append(pret)
                    elif luna == "Sep":
                        dictProd[Nume][9].append(pret)
                    elif luna == "Oct":
                        dictProd[Nume][10].append(pret)
                    elif luna == "Noi":
                        dictProd[Nume][11].append(pret)
                    else: dictProd[Nume][12].append(pret)
        #daca nu are valori in anul respectiv e sters
        if valid:
            for i in range(12):
                if dictProd[Nume][i + 1]:
                    dictProd[Nume][i + 1] = round(sum(dictProd[Nume][i + 1]) / len(dictProd[Nume][i + 1]), 2)
                else: dictProd[Nume][i + 1] = None
        else: del dictProd[Nume]

        indexNext = data.find("label", indexNext + 1)
    return dictProd

def lista_store(prod_x):
    for store in prod_x.keys():
        luna = 1
        while prod_x[store][luna] == None:
            luna += 1
        else:
            vinit = prod_x[store][luna]
        for x in prod_x[store].keys():
            if prod_x[store][x] != None:
                prod_x[store][x] = round((prod_x[store][x] - vinit)*100/vinit, 2)
    return prod_x

url = 'https://www.istoric-preturi.info/pd/19463161/MHDA3RM/A/telefon-mobil-iphone-11-64gb-fara-incarcator-si-casti-black'

f = open("citire.txt")

#dictMag = {NumeMag : {luna : [suma val tuturor produselor din acea luna, nr de val]}}
for line in f:
    dictProd = inputProd(line)
    dictProd = lista_store(dictProd)
    for x in dictProd.keys():
        if x in dictMag:
            for i in range(12):
                if dictProd[x][i + 1]:
                    dictMag[x][i + 1][0] += dictProd[x][i + 1]
                    dictMag[x][i + 1][1] += 1
        else:
            dictMag[x] = {i + 1 : [dictProd[x][i + 1] if dictProd[x][i + 1] else 0, 1] for i in range(12)}
#media aritmetica pe fiecare luna
for x in dictMag.keys():
    for i in range(12):
        dictMag[x][i + 1] = round(dictMag[x][i + 1][0] / dictMag[x][i + 1][1], 2)

print(dictMag)


