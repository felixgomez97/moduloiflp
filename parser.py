
sql="SELECT S.*, P.*, C.*, CO.*, T.* "\
		"FROM SUBSCRIPTION S "\
		"INNER JOIN PARTICIPANT P "\
			"ON P.NAME = S.NAME "\
		"INNER JOIN COMPANY C "\
			"ON C.COMPANY = P.COMPANY "\
		"INNER JOIN COURSE CO "\
			"ON CO.COURSE = S.COURSE "\
		"INNER JOIN TOPIC T "\
			"ON T.TOPIC = CO.TOPIC;"

sentencia_column_name = "SELECT column_name"\
						" FROM information_schema.columns"\
						" WHERE table_schema = 'public'"\
						" AND table_name = "

def parser(sql):
	#Se separa el string SQL por el token "espacio" en una lista
	sql_list = sql.split(' ')
	print(sql_list)
	print("\n")

	# Se obtiene el nombre de la TABLA BASE	
	a = 0
	for i in sql_list :
		if i == 'FROM':
			tabla_base = sql_list[a+1]
			tabla_base_apodo = sql_list[a+2]
			break
		a = a+1

	# Se obtiene el nombre de las demas tablas
	# Se almacena en una lista, se guarda NOMBRE, APODO
	a = 0
	lista_tablas = []
	for i in sql_list :
		if i == 'JOIN':
			lista_tablas.append(sql_list[a+1])
			lista_tablas.append(sql_list[a+2])
		a = a+1

	print("Tabla base: " + tabla_base + ", " +tabla_base_apodo + "\n")
	print("Lista de tablas:")
	print(lista_tablas)
	print("\n")

	#------------------------------------------------------
	# Basado en los nombres de tablas, se obtiene de cada una
	# los nombres de sus columnas en el orden que corresponde

	diccionario_columnas = {}
	# Dicho diccionario tendrá como clave el nombre de tabla
	# Y el contenido será la tupla de nombre de columnas

	sentencia1 = sentencia_column_name + tabla_base + ";"
	print(sentencia1)
	# Aqui se EJECUTA la SENTENCIA1 y lo que retorne se almacena
	# Se asume que la variable COLUMNAS almacena el resultado del query
	"columnas.execute(sentencia1)"

	'''
	lista_columnas = []
	elemento = columnas.fetchone()
 	
    while elemento is not None:
    	lista_columnas.append(elemento)
        elemento = columnas.fetchone()

	diccionario_columnas[tabla_base] = lista_columnas
	'''


	#Lo mismo pero para el resto de las tablas
	for i in range(0, len(lista_tablas), 2):
		sentencia = sentencia_column_name + lista_tablas[i] + ";"
		print(sentencia)
		# Aqui se EJECUTA la SENTENCIA y lo que retorne se almacena
		# Se asume que la variable COLUMNAS almacena el resultado del query
		"columnas.execute(sentencia)"
		'''		
		lista_columnas = []
		elemento = columnas.fetchone()
	 	
	    while elemento is not None:
	    	lista_columnas.append(elemento)
	        elemento = columnas.fetchone()

		diccionario_columnas[lista_tablas[i]] = lista_columnas
		'''


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


"-----------------------------------------------------------------------------"

#Se ejecuta la función PARSER
parser(sql)


"-----------------------------------------------------------------------------"

#Copia de la consulta hecha en PGADMIN3
#"adams";"srw";"adams";"researcher";"scuf";"no";23;"scuf";"university";"srw";3;"advanced";"ilp";"ilp";f;"muggleton"
#"blake";"cso";"blake";"president";"jvt";"yes";5;"jvt";"commercial";"cso";2;"introductory";"database";"database";t;"george"
