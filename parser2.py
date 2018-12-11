from connection import *
import re

sql="SELECT S.*, P.*, C.*, CO.*, T.* "\
		"FROM SUBSCRIPTION S "\
		"INNER JOIN PARTICIPANT P "\
			"ON P.NAME = S.ID_PARTICIPANT "\
		"INNER JOIN COMPANY C "\
			"ON C.COMPANY = P.ID_COMPANY "\
		"INNER JOIN COURSE CO "\
			"ON CO.COURSE = S.ID_COURSE "\
		"INNER JOIN TOPIC T "\
			"ON T.TOPIC = CO.ID_TOPIC;"

sentencia_column_name = "SELECT column_name"\
						" FROM information_schema.columns"\
						" WHERE table_schema = 'public'"\
						" AND table_name = "

sql_foreign = "SELECT 	TC.CONSTRAINT_NAME, "\
				"KCU_referenciado.TABLE_NAME, "\
				"KCU_referenciado.COLUMN_NAME, "\
				"TC.TABLE_NAME, "\
				"KCU_fuente.COLUMN_NAME "\
					"FROM information_schema.table_constraints TC "\
					  "INNER JOIN information_schema.referential_constraints RC "\
						"ON RC.CONSTRAINT_NAME = TC.CONSTRAINT_NAME "\
					  "INNER JOIN information_schema.key_column_usage KCU_referenciado "\
						"ON KCU_referenciado.CONSTRAINT_NAME = RC.UNIQUE_CONSTRAINT_NAME "\
					  "INNER JOIN information_schema.key_column_usage KCU_fuente "\
						"ON KCU_fuente.CONSTRAINT_NAME = RC.CONSTRAINT_NAME;" 

def parser(sql):
	#Se separa el string SQL por el token "espacio" en una lista
	sql_list = sql.split(' ')
	#Se borran las "comas" del SELECT en la lista sql_list
	a = 0
	for i in sql_list :
		sql_list[a] = sql_list[a].replace(",", "")
		a = a+1

	print(sql_list)
	print("\n")


	"---------------------------NOMBRES DE TABLAS-----------------------------"
	# Se obtiene el nombre de la TABLA BASE	y APODO
	a = 0
	lista_tablas = []
	for i in sql_list :
		if i == 'FROM':
			lista_tablas.append(sql_list[a+1])
			lista_tablas.append(sql_list[a+2])
			break
		a = a+1

	# Se obtiene el nombre de las demas tablas
	# Se almacena en la misma lista, se guarda NOMBRE, APODO
	a = 0
	for i in sql_list :
		if i == 'JOIN':
			lista_tablas.append(sql_list[a+1])
			lista_tablas.append(sql_list[a+2])
		a = a+1

	print("Lista de tablas:")
	print(lista_tablas)
	print("\n")


	"--------------------------NOMBRES DE COLUMNAS----------------------------"
	# Basado en los nombres de tablas, se obtiene de cada una
	# los nombres de sus columnas en el orden que corresponde

	diccionario_columnas = {}
	# Dicho diccionario tendrá como clave el nombre de tabla
	# Y el contenido será la tupla de nombre de columnas
	
	bd = Connection("registration")
	columnas = bd.conn.cursor()

	for i in range(0, len(lista_tablas), 2):
		sentencia = sentencia_column_name + "LOWER('%s')"%lista_tablas[i] + ";"
		print(sentencia)
		# Aqui se EJECUTA la SENTENCIA y lo que retorne se almacena
		# Se asume que la variable COLUMNAS almacena el resultado del query
		columnas.execute(sentencia)

		lista_columnas = []
		elemento = columnas.fetchone()

		while elemento is not None:
			lista_columnas.append(elemento)
			elemento = columnas.fetchone()

		diccionario_columnas[lista_tablas[i]] = lista_columnas

	print("\nLista de Tablas con sus respectivas columnas:\n")

	for tabla in diccionario_columnas:
		print(tabla, ": ", diccionario_columnas[tabla])

	'''
	En esas dos partes comentadas de esta misma manera se pretende:
		- Obtener los nombres de las columnas de cada una de las tablas
		- Eso se realiza mediante una sentencia de Postgres almacenado en
			la variable "sentencia_column_name"
		- El procedimiento de FETCH se hace en base al ejemplo encontrado
			en el link: http://www.postgresqltutorial.com/postgresql-python/query/
		- El query lo que hace es retornar los nombres de las columnas como 
			registros que se tienen que ir recorriendo con FETCH, a la par
			ir almacenando dentro de LISTA_COLUMNAS para luego almacenarlo en 
			el DICCIONARIO_COLUMNAS, que se tiene como clave el nombre de la tabla
			y el contenido es la lista de las columnas de dicha tabla
	'''

	"--------------------------RELACIONES FORANEAS----------------------------"
	#Relaciones de clave foránea
	foraneos = bd.conn.cursor()
	foraneos.execute(sql_foreign)
	foraneo = foraneos.fetchone()
	lista_foraneos = []
	
	while foraneo is not None:
		lista_foraneos.append(foraneo)
		foraneo = foraneos.fetchone()

	print("\nLista de relaciones de clave foranea:")
	print("constraint - tabla origen - columna origen - tabla destino - columna destino")
	print(lista_foraneos)
	print("\n")


	"-----------------GENERAR TUPLA CON NOMBRES DE COLUMNAS-------------------"
	tupla_columnas = []

	for tabla in sql_list:
		nombre_tabla = tabla.replace(".*", "")
		for i in range(0, len(lista_tablas), 2):
			if (nombre_tabla == lista_tablas[i]):
				tupla_columnas.append(diccionario_columnas[nombre_tabla])

	print("#############################################")
	print(tupla_columnas)

	"---------------------------CONSULTA DE DATOS-----------------------------"
	#Datos de la BD
	datos = bd.conn.cursor()
	datos.execute(sql)

	lista_hechos = []
	hecho = ""
	

	diccionario_datos = {}
	elemento = datos.fetchone()

	while elemento is not None:
		print("- - - - - - - - - COLUMNAS - - - - - - - - - -")
		print(tupla_columnas)
		print("- - - - - - - - - ELEMENTO - - - - - - - - - -")
		print(elemento)

		a = 0
		for j in range(0, len(tupla_columnas)-1):
			for k in range(0, len(tupla_columnas[j])):
				#print(str(a)+"-----tupla-----"+str(j)+"-----columnas-----"+str(k))
				#print(tupla_columnas[j])
				#print(tupla_columnas[j][k])
				#print(tupla_columnas[j][k][0])

				diccionario_datos[tupla_columnas[j][k][0]] = elemento[a]
				a = a+1

		print("- - - - - - - - - - - - - - - - - - - - - - - -")
		print("- - - - - - - - - - MERGE - - - - - - - - - - -")
		print("- - - - - - - - - - - - - - - - - - - - - - - -")
		print(diccionario_datos)		
		print("\n")
		
		
		"---- construccion del hecho -------"
		hecho = lista_tablas[0] + "("




		elemento = datos.fetchone()
		lista_hechos.append(hecho)

	'''
	while elemento is not None:
		hecho = lista_tablas[0] + "("
		
		
		for tabla in diccionario_columnas:
			hecho = hecho + tabla + "("
		

		
		print(hecho)
	'''
	
	for i in lista_hechos:
		print(i)


"----------------------------EJECUCIÓN DEL MÓDULO-----------------------------"

#Se ejecuta la función PARSER
parser(sql)


"------------------------------------FIN--------------------------------------"

#Copia de la consulta hecha en PGADMIN3
#"adams";"srw";"adams";"researcher";"scuf";"no";23;"scuf";"university";"srw";3;"advanced";"ilp";"ilp";f;"muggleton"
#"blake";"cso";"blake";"president";"jvt";"yes";5;"jvt";"commercial";"cso";2;"introductory";"database";"database";t;"george"

'''
Producto final - HECHO
SUBSCRIPTION( PARTICIPANT(adam, researcher, COMPANY(scuf, university), 23),
			  COURSE(erm, 3, introductory, TOPIC(database, true, george))) = no
'''