
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

columnname = "SELECT column_name"\
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
	list_tablas = []
	for i in sql_list :
		if i == 'JOIN':
			list_tablas.append(sql_list[a+1])
			list_tablas.append(sql_list[a+2])
		a = a+1

	print("Tabla base: " + tabla_base + ", " +tabla_base_apodo + "\n")
	print("Lista de tablas:")
	print(list_tablas)

#Se ejecuta la función PARSER
parser(sql)

#"adams";"srw";"adams";"researcher";"scuf";"no";23;"scuf";"university";"srw";3;"advanced";"ilp";"ilp";f;"muggleton"
#"blake";"cso";"blake";"president";"jvt";"yes";5;"jvt";"commercial";"cso";2;"introductory";"database";"database";t;"george"
