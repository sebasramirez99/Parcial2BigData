import json
import requests
import time
import boto3

#nombreEmpresa del bucket donde se va a guardar todas las descargas de:
# elespectador
# eltiempo


bucket="parcial2-punto2-02091999"

# funcion principal 
def handler(event, context):
	
	#funcion que devuelve el formato de la hora local
	tiempo = time.localtime()
	
	# Obtener recursos de la sesión predeterminada
	s3 = boto3.resource('s3')

	#llamamos a la funcion optener para cada una de las paginas
	optener("elespectador",tiempo,bucket,s3,"https://www.elespectador.com/")
	optener("eltiempo",tiempo,bucket,s3,"https://www.eltiempo.com/")
	return {
	'statusCode':200,
	'body': json.dumps('Hello from Lambda')
	}

#funciion encargada de agregar los datos respectivos al bucket 
#funciion encargada de agregar los datos respectivos al bucket 
def optener(nombreEmpresa,tiempo,bucketN,s3,urlYahoo):
	headers = {'User-Agent': 'Mozilla'}

	# pasamos a la variable r lo que obtenemos de la url  
	r = requests.get(urlYahoo, headers=headers)

	#declaramos una variable con la direccion del archivo
	DireccionArchivo="/tmp/"+nombreEmpresa+".txt"

	f = open(DireccionArchivo,"w")
	print("Saving...")
	f.write(r.text)
	f.close()

	# direccion donde se va a guardar con la estructura: s3://bucket/stocks/company=xxx/year=xxx/month=xxx/day=xxx
	d = 'headlines/raw/periodico='+nombreEmpresa+'/year='+str(tiempo.tm_year)+'/month='+str(tiempo.tm_mon)+'/day='+str(tiempo.tm_mday)+'/'+nombreEmpresa+'.txt'
	
    # sube el archivo al bucket parcial2-punto1-02091999 con la direccion d 
	s3.meta.client.upload_file(DireccionArchivo,bucketN,d)




