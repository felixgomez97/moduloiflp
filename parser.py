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


def constructor(hecho, inicio, lista_tablas, diccionario_columnas, 
				lista_foraneos, diccionario_datos):
	print(diccionario_columnas)
	print("\n")
	print(diccionario_datos)
	print("\n")

	#Metodo para ordenar Lista de Foraneos de relaciones más a menos atómicas 
	for i in range(0, len(lista_foraneos)):
		tablaorigen = lista_foraneos[i][3]
		for j in range(0, len(lista_foraneos)):
			tabladestino = lista_foraneos[j][1]
			if tablaorigen == tabladestino :
				aux = lista_foraneos[j]
				lista_foraneos[j] = lista_foraneos[i]
				lista_foraneos[i] = aux


	print("\n---------------------------------\n")
	print("TablaOrigen - ColumnaOrigen - TablaDestino - ColumnaDestino")
	for lf in lista_foraneos :
		print(lf[1]+" - "+lf[2]+" - "+lf[3]+" - "+lf[4])
	print("\n")



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

	#input()

	#FORANEOS
	#constraint - tabla origen - columna origen - tabla destino - columna destino
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
					columna_origen = relacion[2]
					columna_destino = relacion[4]
					columna_posicion_base = posicion
				elif (split_hecho_tabla_base[posicion] == relacion[3]) and (tabla_posicion_base == -1): 
					tabla_origen = relacion[1]
					tabla_destino = relacion[3]
					tabla_posicion_base = posicion
				
				if tabla_posicion_base != -1 and columna_posicion_base != -1 :
					break
			if tabla_posicion_base != -1 and columna_posicion_base != -1 :
				break

		'''	Impresiones de prueba/verificación	
		print("\n----- Nombres de Tablas/Columnas -----")	
		print("tabla_origen: "+tabla_origen)
		print("columna_origen: "+columna_origen)
		print("tabla_destino: "+tabla_destino)
		print("columna_destino: "+columna_destino)
		print("\n----- Posiciones -----")
		print("tabla_posibase: "+str(tabla_posicion_base))
		print("columna_posibase: "+str(columna_posicion_base))
		'''

		'''
			ACLARACIÓN
		Paralelamente se construye el hecho con los datos de la consulta
		se construye el hecho con los nombres de las tablas y columnas
		a fin de poder ir consultando en cada iteración las posiciones
		relativas
		'''

		#Construccion de Hecho
		print("\n----- Construccion de Hecho -----")
		for posicion_destino in range(0, len(lista_hechos_tabla)) :
			split_destino = lista_hechos_tabla[posicion_destino].split(' ')
			#Se replica lo mismo para la tabla base
			split_destino_base = lista_hechos_tabla_base[posicion_destino].split(' ')

			for tabla in split_destino :
				if tabla == tabla_destino :
					#Nos posicionamos sobre la columna destino
					#Buscando el correspondiente contenido 
					columna_destino = split_destino[columna_posicion_base]
					columna_destino_base = split_destino_base[columna_posicion_base]

					contenido_origen = ""
					for posicion_origen in range(0, len(lista_hechos_tabla)) :
						split_origen = lista_hechos_tabla[posicion_origen].split(' ')
						#Se replica lo mismo para la tabla base
						split_origen_base = lista_hechos_tabla_base[posicion_origen].split(' ')

						for tabla_ori in split_origen:
							if tabla_ori == tabla_origen:
								contenido_origen = lista_hechos_tabla[posicion_origen]
								contenido_origen_base = lista_hechos_tabla_base[posicion_origen]
								#break

					'''	Impresiones de prueba/verificación		
					print("contenido_origen: " + contenido_origen)
					print("\tcontenido_origen_base: " + contenido_origen_base)
					print("contenido_destino: " + str(lista_hechos_tabla[posicion_destino]))					
					print("tabla_destino: " + tabla)					
					print("columna_destino: " + columna_destino)
					print("posicion_destino: " + str(posicion_destino))
					'''
					lista_hechos_tabla[posicion_destino] = lista_hechos_tabla[posicion_destino].replace(columna_destino,contenido_origen)
					lista_hechos_tabla_base[posicion_destino] = lista_hechos_tabla_base[posicion_destino].replace(columna_destino_base,contenido_origen_base)
					print("\nColumna substituida:\n" + str(lista_hechos_tabla[posicion_destino]))
					print("\nColumna BASE substituida:\n" + str(lista_hechos_tabla_base[posicion_destino]))

		print("\n---------------------------------\n")
		#input()

	hecho = lista_hechos_tabla[0]
	return hecho


#Función principal PARSER
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
		lista = []
		for valor in foraneo:
			lista.append(valor)
		lista_foraneos.append(lista)
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

		elemento = datos.fetchone()
		lista_hechos.append(hecho)


	print("\n------------------- HECHOS -------------------")
	for i in lista_hechos:
		print(i + "\n")



"----------------------------EJECUCIÓN DEL MÓDULO-----------------------------"

#Ejecución de la función PARSER
parser(sql)


"------------------------------------FIN--------------------------------------"