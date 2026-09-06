import sqlite3
import unittest
from pathlib import Path
from unittest.mock import patch

from db import _migrar_modulo
from repositories.calificaciones import (
    borrar_calificacion,
    get_contexto_calificacion,
    guardar_calificacion,
)


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "backend" / "schema.sql"


class TestCalificaciones(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.conn.execute('INSERT INTO "Estudiante" (nombre) VALUES (?)', ("Ana",))
        self.conn.execute(
            'INSERT INTO "Actividad" (codigo, nombre) VALUES (?, ?)',
            ("AC1", "Actividad 1"),
        )
        self.conn.commit()
        self.patch_get_connection = patch(
            "repositories.calificaciones.get_connection",
            side_effect=lambda modulo: self.conn,
        )
        self.patch_get_connection.start()

    def tearDown(self):
        self.patch_get_connection.stop()
        self.conn.close()

    def test_guarda_y_recupera_evaluacion_sin_calificaciones(self):
        guardar_calificacion("modulo-prueba", 1, 1, [], "Buen trabajo")

        contexto = get_contexto_calificacion("modulo-prueba", 1, 1)

        self.assertEqual(contexto["items"], [])
        self.assertEqual(contexto["evaluacion"], "Buen trabajo")

    def test_actualiza_y_borra_evaluacion(self):
        guardar_calificacion("modulo-prueba", 1, 1, [], "Primera evaluación")
        guardar_calificacion("modulo-prueba", 1, 1, [], "Segunda evaluación")

        self.assertEqual(
            get_contexto_calificacion("modulo-prueba", 1, 1)["evaluacion"],
            "Segunda evaluación",
        )
        self.assertTrue(borrar_calificacion("modulo-prueba", 1, 1))
        self.assertIsNone(
            get_contexto_calificacion("modulo-prueba", 1, 1)["evaluacion"]
        )

    def test_evaluacion_respeta_claves_externas(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                'INSERT INTO "Evaluacion" VALUES (?, ?, ?)',
                (99, 1, "Texto"),
            )


class TestMigracionEvaluacion(unittest.TestCase):

    def test_migra_desde_version_uno(self):
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.execute('DROP TABLE "Evaluacion"')
        conn.execute(
            'UPDATE "Metadatos" SET valor = ? WHERE clave = \'db_version\'',
            ("1",),
        )

        _migrar_modulo(conn)

        self.assertIsNotNone(
            conn.execute(
                'SELECT 1 FROM sqlite_master WHERE type = \'table\' AND name = \'Evaluacion\''
            ).fetchone()
        )
        self.assertEqual(
            conn.execute(
                'SELECT valor FROM "Metadatos" WHERE clave = \'db_version\''
            ).fetchone()[0],
            "2",
        )
        conn.close()


if __name__ == "__main__":
    unittest.main()
