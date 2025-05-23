from datetime import datetime

class Llibre:
    def __init__(self, isbn="None", titol="None", autor="None", dni_prestec="0", data_prestec=None):
        self.isbn = isbn
        self.titol = titol
        self.autor = autor
        self.dni_prestec = dni_prestec
        self.data_prestec = data_prestec or datetime.now().date()

    def introduir_dades(self):
        self.isbn = input("ISBN: ").strip()
        self.titol = input("Títol: ").strip()
        self.autor = input("Autor: ").strip()
        if not all([self.isbn, self.titol, self.autor]):
            print("Error: Camps obligatoris.")
            self.introduir_dades()