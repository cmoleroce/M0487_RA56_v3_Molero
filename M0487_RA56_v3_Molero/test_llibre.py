import unittest
from datetime import datetime, timedelta
from llibre import Llibre

class TestLlibre(unittest.TestCase):
    
    def test_creacio_basica(self):
        llibre = Llibre("978849123", "El Senyor dels Anells", "J.")
        self.assertEqual(llibre.isbn, "978849123")
        self.assertEqual(llibre.titol, "El Senyor dels Anells")
        self.assertEqual(llibre.autor, "J.")
        self.assertEqual(llibre.dni_prestec, "0") 

    def test_dies_restants_prestat(self):
        data_prestec = datetime.now().date() - timedelta(days=25)
        llibre = Llibre(
            isbn="978123456", 
            dni_prestec="12345678Z", 
            data_prestec=data_prestec
        )
        
        self.assertEqual(llibre.dies_restants(), 5)  

    def test_llibre_disponible(self):
        llibre = Llibre("978000000", "1984", "Jorge")
        self.assertEqual(llibre.dies_restants(), 0)

    def test_imprimir_dades(self):
        llibre = Llibre("978045152", "Rebel", "Jorge")
        import io
        from contextlib import redirect_stdout
        
        with io.StringIO() as buffer, redirect_stdout(buffer):
            llibre.imprimir_dades()
            output = buffer.getvalue().strip()
            
        self.assertIn("Disponible", output)
        self.assertIn("Rebel", output)

if __name__ == '__main__':
    unittest.main()