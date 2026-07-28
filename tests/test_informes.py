import sqlite3
import unittest
from pathlib import Path
from unittest.mock import patch

from repositories.informes import get_listado_indicadores


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "backend" / "schema.sql"


class TestListadoIndicadores(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.patch_get_connection = patch(
            "repositories.informes.get_connection",
            side_effect=lambda modulo: self.conn,
        )
        self.patch_get_connection.start()

    def tearDown(self):
        self.patch_get_connection.stop()
        self.conn.close()

    def test_agrupa_indicadores_y_conserva_pesos(self):
        self.conn.execute(
            'INSERT INTO "Resultado" (codigo, nombre, peso) VALUES (?, ?, ?)',
            ("RA1", "Resultado 1", 4),
        )
        self.conn.execute(
            'INSERT INTO "Indicador" (codigo, nombre) VALUES (?, ?)',
            ("IL1", "Indicador 1"),
        )
        self.conn.execute(
            'INSERT INTO "Indicador_Resultado" (id_indicador, id_resultado, peso) VALUES (?, ?, ?)',
            (1, 1, 3),
        )
        self.conn.commit()

        informe = get_listado_indicadores("modulo-prueba")

        self.assertEqual(informe["modulo"], "modulo-prueba")
        self.assertEqual(len(informe["resultados"]), 1)
        resultado = informe["resultados"][0]
        self.assertEqual(resultado["peso"], 4)
        self.assertEqual(resultado["indicadores"][0]["codigo"], "IL1")
        self.assertEqual(resultado["indicadores"][0]["peso"], 3)

    def test_informe_sin_resultados_devuelve_lista_vacia(self):
        informe = get_listado_indicadores("modulo-prueba")

        self.assertEqual(informe["resultados"], [])


if __name__ == "__main__":
    unittest.main()
