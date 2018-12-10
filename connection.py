import psycopg2


class Connection():
	#Se define el constructor de la clase, requiere como argumento la base de datos a dónde se quiere realizar la conexión
	def __init__(self,PSQL_DB):
		self.conn = self.tryconn(PSQL_DB)

	#Se define la función que intentará realizar la conexión
	def tryconn(self,PSQL_DB):
		# Variables Postgres
		PSQL_HOST = "localhost"
		PSQL_PORT = "5432"
		PSQL_USER = "postgres"
		PSQL_PASS = "postgres"

		try:
		    # Se intenta la conexión a la base de datos
			connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
			conn = psycopg2.connect(connstr)
			return conn

		except (Exception, psycopg2.DatabaseError) as e:
			print(e)
