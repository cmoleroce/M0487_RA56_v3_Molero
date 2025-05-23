import unittest
import sqlite3
import os
from usuari import Usuari
from gestio_biblioteca import Biblioteca

class TestBiblioteca(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_name = 'test_biblioteca.db'
        if os.path.exists(cls.db_name):
            os.remove(cls.db_name)
            
        cls.biblio = Biblioteca()
        cls.biblio.conn = sqlite3.connect(cls.db_name)
        cls.biblio.crear_taules()