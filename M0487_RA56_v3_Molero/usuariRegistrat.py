import hashlib
from getpass import getpass
from usuari import Usuari

class UsuariRegistrat(Usuari):
    def __init__(self, **kwargs):
        super().__init__(
            dni=kwargs.get('dni', 'None'),
            nom=kwargs.get('nom', 'None'),
            cognoms=kwargs.get('cognoms', 'None')
        )
        self._contrasenya = self._encriptar(kwargs.get('contrasenya', ''))
        self.tipus_usuari = kwargs.get('tipus_usuari', 'lector').lower()

    def _encriptar(self, contrasenya):
        return hashlib.sha256(contrasenya.encode()).hexdigest()

    def introduir_dades(self):
        super().introduir_dades()
        contrasenya_plana = getpass("Contrasenya: ")
        self._contrasenya = self._encriptar(contrasenya_plana)
        self.tipus_usuari = 'lector'