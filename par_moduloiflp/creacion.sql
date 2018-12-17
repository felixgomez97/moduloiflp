
CREATE TABLE public.Usuario (
                id_usuario INTEGER NOT NULL,
                login_name VARCHAR(100) NOT NULL,
                contrasena VARCHAR NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                tipo_usuario INTEGER NOT NULL,
                correo VARCHAR(100) NOT NULL,
                CONSTRAINT usuario_pk PRIMARY KEY (id_usuario)
);


CREATE TABLE public.TransaccionCab (
                id_transaccion INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                fecha VARCHAR NOT NULL,
                total INTEGER NOT NULL,
                direccion_envio VARCHAR(100) NOT NULL,
                estado VARCHAR(1) NOT NULL,
                medio_de_pago INTEGER NOT NULL,
                nro_tarjeta INTEGER NOT NULL,
                estado_1 VARCHAR NOT NULL,
                CONSTRAINT transaccioncab_pk PRIMARY KEY (id_transaccion)
);


CREATE TABLE public.Categorias (
                id_categoria VARCHAR(30) NOT NULL,
                nombre_categoria VARCHAR(100) NOT NULL,
                CONSTRAINT categorias_pk PRIMARY KEY (id_categoria)
);


CREATE TABLE public.Productos (
                id_producto VARCHAR(30) NOT NULL,
                Cantidad INTEGER NOT NULL,
                descripcion VARCHAR(500) NOT NULL,
                PrecioUnit INTEGER NOT NULL,
                nombre_img VARCHAR(100) NOT NULL,
                id_categoria VARCHAR(30) NOT NULL,
                CONSTRAINT productos_pk PRIMARY KEY (id_producto)
);


CREATE TABLE public.TransaccionDet (
                id_transaccion INTEGER NOT NULL,
                id_producto VARCHAR(30) NOT NULL,
                cantidad INTEGER NOT NULL,
                precio INTEGER NOT NULL,
                subtotal INTEGER NOT NULL,
                CONSTRAINT transacciondet_pk PRIMARY KEY (id_transaccion)
);


ALTER TABLE public.TransaccionCab ADD CONSTRAINT usuario_carrito_fk
FOREIGN KEY (id_usuario)
REFERENCES public.Usuario (id_usuario)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.TransaccionDet ADD CONSTRAINT transaccioncab_transacciondet_fk
FOREIGN KEY (id_transaccion)
REFERENCES public.TransaccionCab (id_transaccion)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.Productos ADD CONSTRAINT categorias_productos_fk
FOREIGN KEY (id_categoria)
REFERENCES public.Categorias (id_categoria)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.TransaccionDet ADD CONSTRAINT productos_transacciondet_fk
FOREIGN KEY (id_producto)
REFERENCES public.Productos (id_producto)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;



INSERT INTO USUARIO VALUES(100, 'fgomez', 'fg0m3z', 'Gomez', 'Felix', 0, 'fgomez@pol.una.py');
INSERT INTO CATEGORIAS VALUES ('1000', 'Corbata');
INSERT INTO PRODUCTOS VALUES ('1001', 48, 'Corbata Animal Print', 15000, 'corbata_ap.jpg', '1000');
INSERT INTO TRANSACCIONCAB VALUES (100000, 100, '17/12/2018', 30000, 'ASU', '0', 1, 500064, '0');
INSERT INTO TRANSACCIONDET VALUES (100000, '1001', 2, 15000, 30000);

SELECT TD.*, TC.*, U.*, P.*, C.* 
	FROM TRANSACCIONDET TD 
		INNER JOIN TRANSACCIONCAB TC 
			ON TC.ID_TRANSACCION = TC.ID_TRANSACCION 
		INNER JOIN USUARIO U 
			ON U.ID_USUARIO = U.ID_USUARIO 
		INNER JOIN PRODUCTOS P 
			ON P.ID_PRODUCTO = TD.ID_PRODUCTO 
		INNER JOIN CATEGORIAS C 
			ON C.ID_CATEGORIA = P.ID_CATEGORIA;
