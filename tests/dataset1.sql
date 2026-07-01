BEGIN TRANSACTION;

-- Metadatos
INSERT OR IGNORE INTO "Metadatos" VALUES ('app_name','ccxi');
INSERT OR IGNORE INTO "Metadatos" VALUES ('db_version','1');

-- 10 estudiantes
INSERT INTO "Estudiante" (nombre) VALUES
	('Estudiante 1'),
	('Estudiante 2'),
	('Estudiante 3'),
	('Estudiante 4'),
	('Estudiante 5'),
	('Estudiante 6'),
	('Estudiante 7'),
	('Estudiante 8'),
	('Estudiante 9'),
	('Estudiante 10');

-- 5 resultados de aprendizaje
INSERT INTO "Resultado" (codigo, nombre, peso) VALUES
	('RA1', 'Resultado de Aprendizaje 1', 5),
	('RA2', 'Resultado de Aprendizaje 2', 4),
	('RA3', 'Resultado de Aprendizaje 3', 3),
	('RA4', 'Resultado de Aprendizaje 4', 2),
	('RA5', 'Resultado de Aprendizaje 5', 1);

-- 25 indicadores (5 por resultado)
INSERT INTO "Indicador" (codigo, nombre) VALUES
	('IL1.1', 'Indicador de Logro 1.1'),
	('IL1.2', 'Indicador de Logro 1.2'),
	('IL1.3', 'Indicador de Logro 1.3'),
	('IL1.4', 'Indicador de Logro 1.4'),
	('IL1.5', 'Indicador de Logro 1.5'),
	('IL2.1', 'Indicador de Logro 2.1'),
	('IL2.2', 'Indicador de Logro 2.2'),
	('IL2.3', 'Indicador de Logro 2.3'),
	('IL2.4', 'Indicador de Logro 2.4'),
	('IL2.5', 'Indicador de Logro 2.5'),
	('IL3.1', 'Indicador de Logro 3.1'),
	('IL3.2', 'Indicador de Logro 3.2'),
	('IL3.3', 'Indicador de Logro 3.3'),
	('IL3.4', 'Indicador de Logro 3.4'),
	('IL3.5', 'Indicador de Logro 3.5'),
	('IL4.1', 'Indicador de Logro 4.1'),
	('IL4.2', 'Indicador de Logro 4.2'),
	('IL4.3', 'Indicador de Logro 4.3'),
	('IL4.4', 'Indicador de Logro 4.4'),
	('IL4.5', 'Indicador de Logro 4.5'),
	('IL5.1', 'Indicador de Logro 5.1'),
	('IL5.2', 'Indicador de Logro 5.2'),
	('IL5.3', 'Indicador de Logro 5.3'),
	('IL5.4', 'Indicador de Logro 5.4'),
	('IL5.5', 'Indicador de Logro 5.5');

-- Asociar cada indicador a su resultado con peso = número dentro del resultado
INSERT INTO "Indicador_Resultado" (id_indicador, id_resultado, peso) VALUES
	(1,  1, 1), (2,  1, 2), (3,  1, 3), (4,  1, 4), (5,  1, 5),
	(6,  2, 1), (7,  2, 2), (8,  2, 3), (9,  2, 4), (10, 2, 5),
	(11, 3, 1), (12, 3, 2), (13, 3, 3), (14, 3, 4), (15, 3, 5),
	(16, 4, 1), (17, 4, 2), (18, 4, 3), (19, 4, 4), (20, 4, 5),
	(21, 5, 1), (22, 5, 2), (23, 5, 3), (24, 5, 4), (25, 5, 5);

-- 5 actividades entre 15/9/26 y 15/12/26
INSERT INTO "Actividad" (codigo, nombre, fecha) VALUES
	('AC1', 'Actividad 1', '2026-09-15'),
	('AC2', 'Actividad 2', '2026-10-01'),
	('AC3', 'Actividad 3', '2026-10-15'),
	('AC4', 'Actividad 4', '2026-11-15'),
	('AC5', 'Actividad 5', '2026-12-15');

-- Asociar 5 indicadores (solo de RA1, RA2, RA3) a cada actividad con pesos aleatorios (0-3)
-- AC1: IL1.1, IL1.2, IL2.1, IL2.2, IL3.1
INSERT INTO "Indicador_Actividad" (id_indicador, id_actividad, tipo_calificacion, peso) VALUES
	(1,  1, 'ponderada', ABS(RANDOM() % 4)),
	(2,  1, 'ponderada', ABS(RANDOM() % 4)),
	(6,  1, 'ponderada', ABS(RANDOM() % 4)),
	(7,  1, 'ponderada', ABS(RANDOM() % 4)),
	(11, 1, 'ponderada', ABS(RANDOM() % 4));

-- AC2: IL1.3, IL1.4, IL2.3, IL2.4, IL3.2
INSERT INTO "Indicador_Actividad" (id_indicador, id_actividad, tipo_calificacion, peso) VALUES
	(3,  2, 'ponderada', ABS(RANDOM() % 4)),
	(4,  2, 'ponderada', ABS(RANDOM() % 4)),
	(8,  2, 'ponderada', ABS(RANDOM() % 4)),
	(9,  2, 'ponderada', ABS(RANDOM() % 4)),
	(12, 2, 'ponderada', ABS(RANDOM() % 4));

-- AC3: IL1.5, IL2.5, IL3.3, IL3.4, IL3.5
INSERT INTO "Indicador_Actividad" (id_indicador, id_actividad, tipo_calificacion, peso) VALUES
	(5,  3, 'ponderada', ABS(RANDOM() % 4)),
	(10, 3, 'ponderada', ABS(RANDOM() % 4)),
	(13, 3, 'ponderada', ABS(RANDOM() % 4)),
	(14, 3, 'ponderada', ABS(RANDOM() % 4)),
	(15, 3, 'ponderada', ABS(RANDOM() % 4));

-- AC4: IL1.1, IL1.3, IL2.1, IL2.3, IL3.3
INSERT INTO "Indicador_Actividad" (id_indicador, id_actividad, tipo_calificacion, peso) VALUES
	(1,  4, 'ponderada', ABS(RANDOM() % 4)),
	(3,  4, 'ponderada', ABS(RANDOM() % 4)),
	(6,  4, 'ponderada', ABS(RANDOM() % 4)),
	(8,  4, 'ponderada', ABS(RANDOM() % 4)),
	(13, 4, 'ponderada', ABS(RANDOM() % 4));

-- AC5: IL1.2, IL1.4, IL2.2, IL2.4, IL3.1
INSERT INTO "Indicador_Actividad" (id_indicador, id_actividad, tipo_calificacion, peso) VALUES
	(2,  5, 'ponderada', ABS(RANDOM() % 4)),
	(4,  5, 'ponderada', ABS(RANDOM() % 4)),
	(7,  5, 'ponderada', ABS(RANDOM() % 4)),
	(9,  5, 'ponderada', ABS(RANDOM() % 4)),
	(11, 5, 'ponderada', ABS(RANDOM() % 4));

COMMIT;
