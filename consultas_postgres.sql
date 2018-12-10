-- INTENTO 1 - sin exito
SELECT distinct TC.constraint_type, TC.constraint_name, RC.unique_constraint_name, TC.table_name, KCU1.column_name, KCU2.column_name 
	FROM information_schema.table_constraints TC
		INNER JOIN information_schema.referential_constraints RC
		  ON RC.constraint_name = TC.constraint_name
		INNER JOIN information_schema.key_column_usage KCU1
		  ON KCU1.table_name = TC.table_name
		INNER JOIN information_schema.key_column_usage KCU2
		  ON KCU2.constraint_name = RC.unique_constraint_name
	WHERE (TC.constraint_type = 'FOREIGN KEY')-- or TC.constraint_type = 'PRIMARY KEY')
	--AND table_name = LOWER('SUBSCRIPTION')
	--AND KCU1.column_name != KCU2.column_name 
	ORDER BY TC.table_name;

-- INTENTO 2 - exitoso
SELECT 	TC.CONSTRAINT_NAME "nombre_constraint", 
	KCU_referenciado.TABLE_NAME "tabla_origen",
	KCU_referenciado.COLUMN_NAME "columna_origen",
	TC.TABLE_NAME "tabla_destino", 
	KCU_fuente.COLUMN_NAME "columna_destino"	
		FROM information_schema.table_constraints TC
		  INNER JOIN information_schema.referential_constraints RC
			ON RC.CONSTRAINT_NAME = TC.CONSTRAINT_NAME
		  INNER JOIN information_schema.key_column_usage KCU_referenciado
			ON KCU_referenciado.CONSTRAINT_NAME = RC.UNIQUE_CONSTRAINT_NAME
		  INNER JOIN information_schema.key_column_usage KCU_fuente
			ON KCU_fuente.CONSTRAINT_NAME = RC.CONSTRAINT_NAME;


SELECT *
	FROM information_schema.table_constraints
	WHERE constraint_schema = 'public'
	AND constraint_type != 'CHECK';

SELECT * 
	FROM information_schema.referential_constraints;

SELECT * FROM information_schema.key_column_usage
	WHERE table_name = LOWER('participant')
	OR table_name = LOWER('company');

SELECT *
	FROM information_schema.tables 
	WHERE table_schema = 'public';

alter table subscription 
rename column name TO id_participant;

alter table subscription 
rename column course TO id_course;

alter table participant
rename column company TO id_company;

alter table course 
rename column topic TO id_topic;
