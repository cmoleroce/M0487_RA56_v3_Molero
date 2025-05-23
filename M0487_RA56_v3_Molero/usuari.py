import re

class Usuari:
    def __init__(self, dni="None", nom="None", cognoms="None"):
        self.dni = dni
        self.nom = nom
        self.cognoms = cognoms

    def introduir_dades(self):
        while True:
            self.dni = input("DNI: ").strip().upper()
            if re.match(r'^\d{8}[A-Z]$', self.dni):
                break
            print("Error: Format DNI incorrecte (8 dígits + lletra).")
        self.nom = input("Nom: ").strip()
        self.cognoms = input("Cognoms: ").strip()
        if not all([self.nom, self.cognoms]):
            print("Error: Camps obligatoris.")
            self.introduir_dades()