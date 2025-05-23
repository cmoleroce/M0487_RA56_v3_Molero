import unittest
import sqlite3
import os
from usuari import Usuari
from llibre import Llibre
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
                
    def test_usuari_valid(self):
        usuari = Usuari("Pere", "Puig", "12345678Z")
        self.assertTrue(usuari.validar_dni("12345678Z"))
        self.assertFalse(usuari.validar_dni("1234567A"))
        
    def test_afegir_usuari(self):
        usuari = Usuari("Pere", "Puig", "12345678Z")
        self.assertTrue(self.biblio.afegir_usuari(usuari))
        self.assertFalse(self.biblio.afegir_usuari(usuari))  
        
    def test_prestec_llibre(self):
        usuari = Usuari("Pere", "Puig", "12345678Z")
        llibre = Llibre("9781234", "Don Quijote", "Cervantes")
        
        self.biblio.afegir_usuari(usuari)
        self.biblio.afegir_llibre(llibre)
        
        result = self.biblio.prestar_llibre("9781234", "12345678Z")
        self.assertEqual(result, "Préstec realitzat")
        
        result = self.biblio.tornar_llibre("9781234")
        self.assertEqual(result, "Devolució realitzada")

if __name__ == '__main__':
    unittest.main()