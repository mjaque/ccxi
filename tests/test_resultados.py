import unittest
import sqlite3
from pathlib import Path
from unittest.mock import patch

from repositories.resultados import create_resultado
from app import CCXIHandler

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "backend" / "schema.sql"


class TestResultadosRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        cls.conn.row_factory = sqlite3.Row
        cls.conn.execute("PRAGMA foreign_keys = ON;")
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        cls.conn.executescript(schema)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        self.mock_get_conn = patch(
            "repositories.resultados.get_connection",
            side_effect=lambda mod: self.conn
        )
        self.mock_get_conn.start()

    def tearDown(self):
        self.mock_get_conn.stop()
        self.conn.execute("DELETE FROM Resultado")
        self.conn.commit()

    def test_repo_crear_con_peso_cero(self):
        resultado = create_resultado("test", "RA0", "Resultado con peso cero", 0)
        self.assertEqual(resultado["peso"], 0)
        self.assertEqual(resultado["codigo"], "RA0")
        self.assertIsNotNone(resultado["id"])

    def test_repo_crear_con_peso_positivo(self):
        resultado = create_resultado("test", "RA1", "Resultado con peso positivo", 5)
        self.assertEqual(resultado["peso"], 5)

    def test_repo_peso_negativo_rechazado(self):
        with self.assertRaises(sqlite3.IntegrityError):
            create_resultado("test", "RA-NEG", "Resultado con peso negativo", -1)


class TestResultadosValidacion(unittest.TestCase):

    def setUp(self):
        self.handler = CCXIHandler.__new__(CCXIHandler)

    def test_validar_peso_positivo_aceptado(self):
        error = self.handler._validar_resultado("RA0", "nombre", 5)
        self.assertIsNone(error)
    
    def test_validar_peso_cero_aceptado(self):
        error = self.handler._validar_resultado("RA0", "nombre", 0)
        self.assertIsNone(error)

    def test_validar_peso_negativo_rechazado(self):
        error = self.handler._validar_resultado("RA0", "nombre", -1)
        self.assertEqual(error, "El peso no puede ser negativo")

    def test_validar_codigo_vacio(self):
        error = self.handler._validar_resultado("", "nombre", 5)
        self.assertEqual(error, "El código es obligatorio")

    def test_validar_nombre_vacio(self):
        error = self.handler._validar_resultado("RA0", "", 5)
        self.assertEqual(error, "El nombre es obligatorio")


if __name__ == "__main__":
    unittest.main()
