
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


def parser(sql):
	print(sql)
	posicion_from = sql.find("FROM")
	posicion_tablabase = posicion_from + 37




parser(sql)

#"adams";"srw";"adams";"researcher";"scuf";"no";23;"scuf";"university";"srw";3;"advanced";"ilp";"ilp";f;"muggleton"
#"blake";"cso";"blake";"president";"jvt";"yes";5;"jvt";"commercial";"cso";2;"introductory";"database";"database";t;"george"
