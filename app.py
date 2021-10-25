import json
import requests
import time
import boto3

#nombreEmpresa del bucket donde se va a guardar todas las descargas cada dia las acciones de:
# Avianca
# Ecopetrol
# Grupo Aval
# Cementos Argos

bucket="parcial2-punto1-02091999"

# funcion principal 
def handler(event, context):
	
	#funcion que devuelve el formato de la hora local
	tiempo = time.localtime()
	
	# Obtener recursos de la sesión predeterminada
	s3 = boto3.resource('s3')

	#llamamos a la funcion optener para cada una de las empresas
	optener("Avianca",tiempo,bucket,s3,"https://query1.finance.yahoo.com/v7/finance/download/AVHOQ?period1=1634601600&period2=1634688000&interval=1d&events=history&includeAdjustedClose=true")
	optener("Ecopetrol",tiempo,bucket,s3,"https://query1.finance.yahoo.com/v7/finance/download/EC?period1=1634774400&period2=1634860800&interval=1d&events=history&includeAdjustedClose=true")
	optener("GrupoAval",tiempo,bucket,s3,"https://query1.finance.yahoo.com/v7/finance/download/AVAL?period1=1634774400&period2=1634860800&interval=1d&events=history&includeAdjustedClose=true")
	optener("CementosArgos",tiempo,bucket,s3,"https://query1.finance.yahoo.com/v7/finance/download/CMTOY?period1=1634774400&period2=1634860800&interval=1d&events=history&includeAdjustedClose=true")

	return {
	'statusCode':200,
	'body': json.dumps('Hello from Lambda')
	}

#funciion encargada de agregar los datos respectivos al bucket 
def optener(nombreEmpresa,tiempo,bucketN,s3,urlYahoo):
	headers = {'User-Agent': 'Mozilla'}

	# pasamos a la variable r lo que obtenemos de la url en yahoo de la empresa 
	r = requests.get(urlYahoo, headers=headers)

	#declaramos una variable con la direccion del archivo
	DireccionArchivo="/tmp/"+nombreEmpresa+".csv"

	f = open(DireccionArchivo,"w")
	print("Saving...")
	f.write(r.text)
	f.close()

	# direccion donde se va a guardar con la estructura: s3://bucket/stocks/company=xxx/year=xxx/month=xxx/day=xxx
	d = 'stocks/company='+nombreEmpresa+'/year='+str(tiempo.tm_year)+'/month='+str(tiempo.tm_mon)+'/day='+str(tiempo.tm_mday)+'/'+str(tiempo.tm_hour)+str(tiempo.tm_min)+str(tiempo.tm_sec)+'page.csv'
	
	# sube el archivo al bucket parcial2-punto1-02091999 con la direccion d 
	s3.meta.client.upload_file(DireccionArchivo,bucketN,d)

