from connection import *
import re
import copy


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




'''
def constructor(hecho, diccionario_columnas, lista_foraneos, diccionario_datos):
	"---- construccion del hecho -------"
	for clave_tabla in diccionario_columnas:
		for i in range(0,len(diccionario_columnas[clave_tabla])):
			columna = diccionario_columnas[clave_tabla][i][0].lower()
			tabla = clave_tabla.lower()

			ban = 0
			for relacion in lista_foraneos:
				if (tabla == relacion[3]) and (columna == relacion[4]):
					ban = 1

			if(ban == 0):
				for relacion in lista_foraneos:
					if(relacion[2] == columna):
						columna_datos = relacion[4]
				hecho = hecho + str(diccionario_datos[columna_datos] + ", ")

	return hecho
'''

'''
def constructor(hecho, inicio, lista_tablas, diccionario_columnas, 
				lista_foraneos, diccionario_datos):
	"---- construccion del hecho -------"
	for a in range(inicio,len(lista_tablas),2):
		clave_tabla = lista_tablas[a]
		for i in range(0,len(diccionario_columnas[clave_tabla])):
			print(diccionario_columnas[clave_tabla])
			print("range(0,len(diccionario_columnas[clave_tabla])) = "+str(i))	
			columna = diccionario_columnas[clave_tabla][i]
			tabla = clave_tabla

			ban = 0
			for relacion in lista_foraneos:
				if (tabla == relacion[3]) and (columna == relacion[4]):
					ban = 1
					diccionario_columnas[clave_tabla].pop(0)
					hecho = constructor(hecho, a, lista_tablas, diccionario_columnas, 
										lista_foraneos, diccionario_datos)

			if(ban == 0):
				for relacion in lista_foraneos:
					if(relacion[2] == columna):
						columna_datos = relacion[4]
				hecho = hecho + str(diccionario_datos[relacion[4]] + ", ")
				print("HECHO -> " + hecho)

	return hecho
'''



'''
Producto final - HECHO
SUBSCRIPTION( PARTICIPANT(adam, researcher, COMPANY(scuf, university), 23),
			  COURSE(erm, 3, introductory, TOPIC(database, true, george))) = no
'''

'''
def constructor(hecho, inicio, lista_tablas, diccionario_columnas, 
				lista_foraneos, diccionario_datos):
	"---- construccion del hecho -------"
	#Itera por los nombres de tablas en el orden del SELECT
	for a in range(inicio, len(lista_tablas),2):
		tabla = lista_tablas[a]
		#Consulta los nombres de columna de cada tabla
		columna_posicion = 0
		for columna in diccionario_columnas[tabla]:
			#Itera para comparar si existe alguna FK con esa tabla/columna
			for foraneos in lista_foraneos:
				if (tabla == foraneos[3] and columna == foraneos[4]):
					#Si existe, vuelve a llamar a la funcion constructor
					#para buscar a mas profundidad
					diccionario_columnas_rec = diccionario_columnas.copy()
					diccionario_columnas_rec[tabla].pop(columna_posicion)

					hecho = hecho + tabla + "( "
					hecho = constructor(hecho, a, lista_tablas.copy(), 
							diccionario_columnas_rec.copy(), 
							lista_foraneos.copy(), diccionario_datos)
					continue

			hecho = hecho + str(diccionario_datos[columna]) + ', '

			columna_posicion = columna_posicion +1

	return hecho
'''

def constructor(hecho, inicio, lista_tablas, diccionario_columnas, 
				lista_foraneos, diccionario_datos):
	print(diccionario_columnas)
	print("\n")
	print(diccionario_datos)
	print("\n")
	print(lista_foraneos)

	lista_hechos_tabla = []
	lista_hechos_tabla_base = []

	for a in range(0, len(lista_tablas),2):
		tabla = lista_tablas[a]
		hecho_tabla = tabla + " ( "
		hecho_tabla_base = tabla + " ( "

		for b in range(0, len(diccionario_columnas[tabla])):
			hecho_tabla = hecho_tabla +\
						  str(diccionario_datos[diccionario_columnas[tabla][b]])

			hecho_tabla_base = hecho_tabla_base +\
								diccionario_columnas[tabla][b]

			if b+1 < len(diccionario_columnas[tabla]) :
				hecho_tabla = hecho_tabla + " , "
				hecho_tabla_base = hecho_tabla_base + " , "

		hecho_tabla = hecho_tabla + " )"
		hecho_tabla_base = hecho_tabla_base + " )"

		lista_hechos_tabla.append(hecho_tabla)
		lista_hechos_tabla_base.append(hecho_tabla_base)

	print("\n")
	for i in lista_hechos_tabla:
		print(i)
	print("\n")
	for i in lista_hechos_tabla_base:
		print(i)

	input()

	for relacion in lista_foraneos:
		#Iteracion dentro de los hechos base con nombres de columnas
		for hecho_tabla_base in lista_hechos_tabla_base:
			#Separacion de palabras por espacios
			split_hecho_tabla_base = hecho_tabla_base.split(' ') 	
			tabla_posicion_base = -1
			columna_posicion_base = -1
			#Busqueda de la posicion relativa a esos datos en el original
			for posicion in range(0,len(split_hecho_tabla_base)):
				if 	(split_hecho_tabla_base[posicion] == relacion[4]) and (columna_posicion_base == -1):
					columna_posicion_base = posicion
				elif (split_hecho_tabla_base[posicion] == relacion[3]) and (tabla_posicion_base == -1): 
					tabla_destino_nombre = relacion[3]
					tabla_posicion_base = posicion
				
				if tabla_posicion_base != -1 and columna_posicion_base != -1 :
					break
			if tabla_posicion_base != -1 and columna_posicion_base != -1 :
				break
		print("tablaposinombre: "+str(tabla_destino_nombre))
		print("tablaposibase: "+str(tabla_posicion_base))
		print("columnaposibase: "+str(columna_posicion_base))

		'''
		#Teniendo las posiciones relativas
		#Se hace la misma busqueda en los hechos iniciales
		for hecho_tabla in lista_hechos_tabla:
			#Separacion de palabras por espacios
			split_hecho_tabla = hecho_tabla.split(' ')
			tabla_posicion = -1
			columna_posicion = -1
			#Busqueda de la posicion relativa a esos datos en el original
			for posicion in range(0,len(split_hecho_tabla)):
				if 	(split_hecho_tabla[posicion] == relacion[2]) and (columna_posicion == -1):
					columna_posicion = posicion
				elif (split_hecho_tabla[posicion] == relacion[1]) and (tabla_posicion == -1): 
					tabla_posicion = posicion
				
				if tabla_posicion != -1 and columna_posicion != -1 :
					break
			if tabla_posicion != -1 and columna_posicion != -1 :
				break
		print("tablaposi: "+str(tabla_posicion))
		print("columnaposi: "+str(columna_posicion))
		'''

		#Construccion de Hecho
		#for i in lista_hechos_tabla :






	return hecho



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
			lista_tablas.append(sql_list[a+1].lower())
			lista_tablas.append(sql_list[a+2].lower())
			break
		a = a+1

	# Se obtiene el nombre de las demas tablas
	# Se almacena en la misma lista, se guarda NOMBRE, APODO
	a = 0
	for i in sql_list :
		if i == 'JOIN':
			lista_tablas.append(sql_list[a+1].lower())
			lista_tablas.append(sql_list[a+2].lower())
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
		nombre_tabla = nombre_tabla.lower()
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
	diccionario_hechos_tabla = {}

	elemento = datos.fetchone()



	for clave_tabla in diccionario_columnas:
		lista = diccionario_columnas[clave_tabla].copy()
		diccionario_columnas[clave_tabla] = []
		for columna_tupla in lista:
			diccionario_columnas[clave_tabla].append(columna_tupla[0])

	print("\nLista de Tablas con sus respectivas columnas:\n")

	for tabla in diccionario_columnas:
		print(tabla, ": ", diccionario_columnas[tabla])



	while elemento is not None:
		a = 0
		for j in range(0, len(tupla_columnas)):
			for k in range(0, len(tupla_columnas[j])):
				#print(str(a)+"-----tupla-----"+str(j)+"-----columnas-----"+str(k))
				#print(tupla_columnas[j])
				#print(tupla_columnas[j][k])
				#print(tupla_columnas[j][k][0])

				diccionario_datos[tupla_columnas[j][k][0]] = elemento[a]
				a = a+1

		print("\n")
		print("- - - - - - - - - - - - - - - - - - - - - - - -")
		print("- - - - - - - - - ELEMENTOS - - - - - - - - - -")
		print("- - - - - - - - - - - - - - - - - - - - - - - -")
		print("\n")

		hecho = lista_tablas[0].lower() + "("
		
		hecho = constructor(hecho, 0, lista_tablas.copy(), 
							copy.deepcopy(diccionario_columnas), 
							lista_foraneos.copy(), diccionario_datos)

		print("\nHECHO -> " + hecho)

		#input()

		elemento = datos.fetchone()
		lista_hechos.append(hecho)

	'''
	while elemento is not None:
		hecho = lista_tablas[0] + "("
		
		
		for tabla in diccionario_columnas:
			hecho = hecho + tabla + "("
		

		
		print(hecho)
	'''


	print("\n------------------- HECHOS -------------------")
	for i in lista_hechos:
		print(i + "\n")



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