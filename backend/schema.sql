BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Metadatos" (
	"clave"	TEXT,
	"valor"	TEXT NOT NULL,
	PRIMARY KEY("clave")
);
INSERT OR IGNORE INTO "Metadatos" VALUES ('app_name','ccxi');
INSERT OR IGNORE INTO "Metadatos" VALUES ('db_version','1');
-- Resultados de Aprendizaje
CREATE TABLE IF NOT EXISTS "Resultado" (
	"id"	INTEGER,
	"codigo"	TEXT UNIQUE NOT NULL,
	"nombre"	TEXT,
	"peso"	INTEGER NOT NULL DEFAULT 1 CHECK (peso >= 0),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Estudiante" (
	"id"	INTEGER,
	"nombre"	TEXT UNIQUE NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
-- Indicadores de Logro
CREATE TABLE IF NOT EXISTS "Indicador" (
	"id"	INTEGER,
	"codigo"	TEXT UNIQUE NOT NULL,
	"nombre"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
-- Actividades Evaluables
CREATE TABLE IF NOT EXISTS "Actividad" (
	"id"	INTEGER,
	"codigo"	TEXT UNIQUE NOT NULL,
	"nombre"	TEXT,
	"fecha"	TEXT 
		CHECK (
			fecha IS NULL
			OR (
				length(fecha) = 10
				AND substr(fecha, 5, 1) = '-'
				AND substr(fecha, 8, 1) = '-'
				AND substr(fecha, 1, 4) GLOB '[0-9][0-9][0-9][0-9]'
				AND substr(fecha, 6, 2) GLOB '[0-9][0-9]'
				AND substr(fecha, 9, 2) GLOB '[0-9][0-9]'
			)
		),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Indicador_Resultado" (
	"id_indicador"	INTEGER NOT NULL,
	"id_resultado"	INTEGER NOT NULL,
	"peso"	INTEGER NOT NULL DEFAULT 1 CHECK (peso >= 0),
	FOREIGN KEY("id_resultado") REFERENCES "Resultado"("id")
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY("id_indicador") REFERENCES "Indicador"("id")
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	PRIMARY KEY("id_indicador", "id_resultado" )
);
CREATE TABLE IF NOT EXISTS "Calificacion" (
	"id_estudiante"	INTEGER NOT NULL,
	"id_indicador"	INTEGER NOT NULL,
	"id_actividad"	INTEGER NOT NULL,
	"nivel_logro" INTEGER,
	"incremento"	REAL,
	FOREIGN KEY("id_estudiante") REFERENCES "Estudiante"("id")
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY("id_indicador") REFERENCES "Indicador"("id")
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY("id_actividad") REFERENCES "Actividad"("id")
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	PRIMARY KEY("id_estudiante", "id_indicador", "id_actividad" )
);
CREATE TABLE IF NOT EXISTS "Indicador_Actividad" (
	"id_indicador"	INTEGER NOT NULL,
	"id_actividad"	INTEGER NOT NULL,
	"tipo_calificacion"	TEXT NOT NULL DEFAULT 'ponderada'
		CHECK (tipo_calificacion IN ('ponderada', 'maxima', 'minima')),
	"peso"	INTEGER CHECK (peso >= 0),
	FOREIGN KEY("id_indicador") REFERENCES "Indicador"("id")
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY("id_actividad") REFERENCES "Actividad"("id")
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	PRIMARY KEY("id_indicador", "id_actividad" )
);
COMMIT;
