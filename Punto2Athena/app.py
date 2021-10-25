import json
import boto3
from warnings import resetwarnings 
import requests
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
s3= boto3.client('s3')
bucket="parcial2-punto2-02091999"

def handler1(event, context):
    tiempo = datetime.datetime.now()
   
    url = "headlines/raw/periodico=eltiempo/year="+str(tiempo.year)+"/month="+str(tiempo.month)+"/day="+str(tiempo.day)+"/eltiempo.txt"
    url1 = "headlines/raw/periodico=elespectador/year="+str(tiempo.year)+"/month="+str(tiempo.month)+"/day="+str(tiempo.day)+"/elespectador.txt"
    response1 = s3.get_object( Bucket=bucket ,Key=url)
    data1 = response1['Body'].read()
    response = s3.get_object(Bucket=bucket,Key=url1)
    data = response['Body'].read()

    e = requests.get('https://www.eltiempo.com').text

    soup = BeautifulSoup(data1,'html.parser')
    link= list()
    titulo= list()
    categoria=list()
    categoria1=list()

    for a in soup.find_all('a',class_="title page-link",href=True):
        categoria.append(str(a['href']))
        link.append("https://www.eltiempo.com"+str(a['href']))

    for a in soup.find_all('a',class_="title page-link"):
        titulo.append(str(a.text))

    for a in range(len(categoria)):
        categoria1.append(categoria[a].split(sep='/')[1])

    print(len(titulo))
    for a in range(len(titulo)):
        print(titulo[a])
        print(link[a])
        print(categoria1[a])

    dict1= {'titulo': titulo, 'categoria':categoria1,'link':link}

    url = 'https://www.elespectador.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    titulo = []

    et =  soup.find_all('h2', class_ = 'Card-Title Title Title')

    for i in soup.find_all('h2', class_ = 'Card-Title Title Title'):
        titulo.append(i.text)

    for i in titulo:
        print(i)

    array = []
    soupS = str(soup)
    vali1 = 82
    valf1 = 86
    lim1 = 188

    vali2 = 112
    valf2 = 116
    lim2 = 215

    vali3 = 108
    valf3 = 112
    lim3 = 218

    vali4 = 4737
    valf4 = 4741
    lim4 = 4835

    vali5 = 4767
    valf5 = 4771
    lim5 = 4840


    for i in soup.find_all('h2', class_ = 'Card-Title Title Title'):
        if str(i)[vali1:valf1] == 'href':
            array.append('https://www.elespectador.com'+str(i)[vali1+6:lim1])
        elif str(i)[vali2:valf2] == 'href':
         array.append('https://www.elespectador.com'+str(i)[vali2+6:lim2])
        elif str(i)[vali3:valf3] == 'href':
            array.append('https://www.elespectador.com'+str(i)[vali3+6:lim3])
        elif str(i)[vali4:valf4] == 'href':
         array.append('https://www.elespectador.com'+str(i)[vali4+6:lim4])
        elif str(i)[vali5:valf5] == 'href':
            array.append('https://www.elespectador.com'+str(i)[vali5+6:lim5])
   

    string = 'rel="noreferrer" target="_self">En Unió'
    txt =''
    bool = False
    link = []
    for i in array:
        var = i[::-1]
        for j in i[::-1]:
            if j == '/':
             bool = True
            if bool == True:
                txt = txt+j
  
        link.append(txt[::-1])
        bool = False
        txt = ''

    for i in link:
        print(i)

    cat = []
    cont = 0
    var = ''


    for i in array:
        for j in i:
            if j == '/':
                cont +=1
            if cont == 3 and j != '/':
                var = var+j
            elif cont == 4:
                cat.append(var)
                cont = 0
                var = ''
                break


    for i in cat:
        print(i)

    for i in cat:
        print(i)
    dict= {'titulo':titulo, 'categoria':cat,'link':link}

    print(len(titulo))
    print(len(link))
    print(len(cat))

    df = pd.DataFrame(dict) 
    df.to_csv('/tmp/espectador.csv')

    for i in cat:
     print(i)

    df1 = pd.DataFrame(dict1) 
    df1.to_csv('/tmp/tiempo.csv')
    url11 = "Headlines/news/periodico=El Tiempo""/year="+str(tiempo.year)+"/month="+str(tiempo.month)+"/day="+str(tiempo.day)+"/Eltiempo.csv"
    s3.upload_file("/tmp/tiempo.csv","parcial2-punto2-2-02091999",url11)
    url12 = "Headlines/news/periodico=El Espectador""/year="+str(tiempo.year)+"/month="+str(tiempo.month)+"/day="+str(tiempo.day)+"/espectador.csv"
    s3.upload_file("/tmp/espectador.csv","parcial2-punto2-2-02091999",url12)

def handler2(event, context):
    bucket_name = 'parcial2-punto2-2-02091999'
    client = boto3.client('athena')
    config = {
        'OutputLocation': 's3://parcial2-punto2-2-02091999/Headlines/news/periodico=El Espectador/year=2021/month=10/',
        'EncryptionConfiguration': {'EncryptionOption': 'SSE_S3'}
    }
    # Query Execution Parameters
    sql = 'MSCK REPAIR TABLE Noticias'
    context = {'Database': 'NoticiasTiempoEspec'}

    client.start_query_execution(QueryString = sql, QueryExecutionContext = context,ResultConfiguration = config)

    config = {
        'OutputLocation': 's3://parcial2-punto2-2-02091999/Headlines/news/periodico=El Tiempo/year=2021/month=10/',
        'EncryptionConfiguration': {'EncryptionOption': 'SSE_S3'}
    }
    # Query Execution Parameters
    sql = 'MSCK REPAIR TABLE noticias2'

    client.start_query_execution(QueryString = sql, QueryExecutionContext = context,ResultConfiguration = config)
