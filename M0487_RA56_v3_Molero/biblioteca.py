from gestio_biblioteca import Biblioteca
from usuariRegistrat import UsuariRegistrat
from menu import MenuAdmin, MenuLector
from getpass import getpass
import hashlib

ADMIN_DEFAULT = {
    "dni": "admin",
    "nom": "Admin",
    "cognoms": "Sistema",
    "contrasenya": "admin123",
    "tipus_usuari": "admin"
}

def iniciar_sessio_o_registre(biblio):
    while True:
        print("\n=== BENVINGUT A LA BIBLIOTECA ===")
        print("1. Iniciar sessió")
        print("2. Registrar-se")
        print("0. Sortir")
        opcio = input("Opció: ").strip()
        if opcio == "1":
            usuari = _iniciar_sessio(biblio)
            if usuari:
                return usuari
        elif opcio == "2":
            _registrar_usuari(biblio)
        elif opcio == "0":
            exit()

def _iniciar_sessio(biblio):
    while True:
        print("\n=== INICI DE SESSIÓ ===")
        dni = input("DNI: ").strip().lower()
        contrasenya = getpass("Contrasenya: ")
        
        cursor = biblio.conn.cursor()
        cursor.execute('SELECT contrasenya, tipus_usuari FROM usuaris WHERE dni = ?', (dni,))
        result = cursor.fetchone()
        
        if result:
            contrasenya_hash = hashlib.sha256(contrasenya.encode()).hexdigest()
            if contrasenya_hash == result[0]:
                return {'dni': dni, 'tipus': result[1]}
        print("Credencials incorrectes.")

def _registrar_usuari(biblio):
    nou_usuari = UsuariRegistrat()
    nou_usuari.introduir_dades()
    if biblio.afegir_usuari(nou_usuari):
        print("Registrat com a lector!")
    else:
        print("Error: DNI ja existeix.")

def crear_admin_inicial(biblio):
    cursor = biblio.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuaris WHERE dni = 'admin'")
    if cursor.fetchone()[0] == 0:
        contrasenya_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO usuaris (dni, nom, cognoms, contrasenya, tipus_usuari)
            VALUES (?, ?, ?, ?, ?)
        ''', ("admin", "Admin", "Sistema", contrasenya_hash, "admin"))
        biblio.conn.commit()
        print("Admin inicial creat.")

def main():
    biblio = Biblioteca()
    crear_admin_inicial(biblio)
    usuari = iniciar_sessio_o_registre(biblio)
    if usuari['tipus'] == 'admin':
        MenuAdmin(biblio, usuari).executar()
    else:
        MenuLector(biblio, usuari).executar()

if __name__ == "__main__":
    main()