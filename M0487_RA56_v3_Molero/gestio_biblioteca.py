import sqlite3
from datetime import datetime
from llibre import Llibre

class Biblioteca:
    def __init__(self):
        self.conn = sqlite3.connect('biblioteca.db')
        self.crear_taules()

    def crear_taules(self):
        cursor = self.conn.cursor()
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuaris (
                dni TEXT PRIMARY KEY,
                nom TEXT,
                cognoms TEXT,
                contrasenya TEXT,
                tipus_usuari TEXT CHECK(tipus_usuari IN ('admin', 'lector'))
            )
        ''')
        # Tabla de libros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS llibres (
                isbn TEXT PRIMARY KEY,
                titol TEXT,
                autor TEXT,
                dni_prestec TEXT DEFAULT '0',
                data_prestec DATE
            )
        ''')
        # Tabla de valoraciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS valoracions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT,
                dni TEXT,
                puntuacio INTEGER,
                FOREIGN KEY(isbn) REFERENCES llibres(isbn)
            )
        ''')
        self.conn.commit()

    def afegir_usuari(self, usuari):
        try:
            self.conn.execute('''
                INSERT INTO usuaris (dni, nom, cognoms, contrasenya, tipus_usuari)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuari.dni, usuari.nom, usuari.cognoms, usuari._contrasenya, usuari.tipus_usuari))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def afegir_llibre(self, llibre):
        try:
            self.conn.execute('''
                INSERT INTO llibres (isbn, titol, autor)
                VALUES (?, ?, ?)
            ''', (llibre.isbn, llibre.titol, llibre.autor))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def eliminar_llibre(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM llibres WHERE isbn = ?', (isbn,))
        self.conn.commit()
        return cursor.rowcount > 0

    def prestar_llibre(self, isbn, dni):
        cursor = self.conn.cursor()
        # Verificar límite de 3 préstamos
        cursor.execute('SELECT COUNT(*) FROM llibres WHERE dni_prestec = ?', (dni,))
        if cursor.fetchone()[0] >= 3:
            return "Màxim 3 llibres per usuari."
        # Verificar préstamos antiguos (>30 días)
        cursor.execute('''
            SELECT julianday('now') - julianday(data_prestec) 
            FROM llibres 
            WHERE dni_prestec = ?
        ''', (dni,))
        for days in cursor.fetchall():
            if days[0] > 30:
                return "Tens préstecs pendents de retornar (més de 30 dies)."
        # Realizar préstamo
        cursor.execute('''
            UPDATE llibres
            SET dni_prestec = ?, data_prestec = DATE('now')
            WHERE isbn = ? AND dni_prestec = "0"
        ''', (dni, isbn))
        self.conn.commit()
        return "Préstec realitzat" if cursor.rowcount > 0 else "No disponible"

    def tornar_llibre(self, isbn):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE llibres
            SET dni_prestec = "0", data_prestec = NULL
            WHERE isbn = ?
        ''', (isbn,))
        self.conn.commit()
        return "Llibre retornat" if cursor.rowcount > 0 else "Error"

    def valorar_llibre(self, isbn, dni, puntuacio):
        try:
            self.conn.execute('''
                INSERT INTO valoracions (isbn, dni, puntuacio)
                VALUES (?, ?, ?)
            ''', (isbn, dni, puntuacio))
            self.conn.commit()
            return "Valoració guardada!"
        except sqlite3.Error:
            return "Error en la valoració."

    def llistar_llibres(self):
        return self.conn.execute('SELECT * FROM llibres').fetchall()

    def llistar_usuaris(self):
        return self.conn.execute('SELECT dni, nom, cognoms, tipus_usuari FROM usuaris').fetchall()

    def modificar_tipus_usuari(self, dni, nou_tipus):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE usuaris
            SET tipus_usuari = ?
            WHERE dni = ?
        ''', (nou_tipus, dni))
        self.conn.commit()
        return cursor.rowcount > 0

    def actualitzar_usuari(self, dni, nom=None, cognoms=None):
        updates = []
        params = []
        if nom:
            updates.append("nom = ?")
            params.append(nom)
        if cognoms:
            updates.append("cognoms = ?")
            params.append(cognoms)
        if not updates:
            return False
        params.append(dni)
        cursor = self.conn.cursor()
        cursor.execute(f'''
            UPDATE usuaris
            SET {', '.join(updates)}
            WHERE dni = ?
        ''', params)
        self.conn.commit()
        return cursor.rowcount > 0

    def actualitzar_llibre(self, isbn, titol=None, autor=None):
        updates = []
        params = []
        if titol:
            updates.append("titol = ?")
            params.append(titol)
        if autor:
            updates.append("autor = ?")
            params.append(autor)
        if not updates:
            return False
        params.append(isbn)
        cursor = self.conn.cursor()
        cursor.execute(f'''
            UPDATE llibres
            SET {', '.join(updates)}
            WHERE isbn = ?
        ''', params)
        self.conn.commit()
        return cursor.rowcount > 0