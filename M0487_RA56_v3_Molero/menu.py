class MenuBase:
    def __init__(self, biblio, usuari):
        self.biblio = biblio
        self.usuari = usuari

    def mostrar_opcions(self):
        raise NotImplementedError

    def processar_opcio(self, opcio):
        raise NotImplementedError

    def executar(self):
        while True:
            self.mostrar_opcions()
            opcio = input("Opció: ").strip()
            if opcio == "0":
                break
            self.processar_opcio(opcio)

class MenuAdmin(MenuBase):
    def mostrar_opcions(self):
        print("\n--- MENÚ ADMIN ---")
        print("1. Gestionar usuaris")
        print("2. Afegir llibre")
        print("3. Eliminar llibre")
        print("4. Modificar llibre")
        print("5. Modificar usuari")
        print("0. Sortir")

    def processar_opcio(self, opcio):
        if opcio == "1":
            self._gestionar_usuaris()
        elif opcio == "2":
            self._afegir_llibre()
        elif opcio == "3":
            self._eliminar_llibre()
        elif opcio == "4":
            self._modificar_llibre()
        elif opcio == "5":
            self._modificar_usuari()

    def _gestionar_usuaris(self):
        while True:
            print("\n--- GESTIÓ D'USUARIS ---")
            print("1. Llistar usuaris")
            print("2. Crear usuari (lector)")
            print("3. Canviar tipus d'usuari")
            print("0. Tornar")
            sub_opcio = input("Opció: ").strip()
            if sub_opcio == "1":
                usuaris = self.biblio.llistar_usuaris()
                for u in usuaris:
                    print(f"DNI: {u[0]} | Nom: {u[1]} {u[2]} | Tipus: {u[3]}")
            elif sub_opcio == "2":
                from usuariRegistrat import UsuariRegistrat
                nou_usuari = UsuariRegistrat()
                nou_usuari.introduir_dades()
                if self.biblio.afegir_usuari(nou_usuari):
                    print("Usuari creat com a lector!")
                else:
                    print("Error: DNI ja existeix.")
            elif sub_opcio == "3":
                dni = input("DNI de l'usuari: ")
                nou_tipus = input("Nou tipus (admin/lector): ").lower()
                if self.biblio.modificar_tipus_usuari(dni, nou_tipus):
                    print("Tipus actualitzat.")
                else:
                    print("Usuari no trobat.")
            elif sub_opcio == "0":
                break

    def _afegir_llibre(self):
        llibre = Llibre()
        llibre.introduir_dades()
        if self.biblio.afegir_llibre(llibre):
            print("Llibre afegit!")
        else:
            print("Error: ISBN repetit.")

    def _eliminar_llibre(self):
        isbn = input("ISBN a eliminar: ")
        if self.biblio.eliminar_llibre(isbn):
            print("Llibre eliminat.")
        else:
            print("No existeix.")

    def _modificar_llibre(self):
        isbn = input("ISBN del llibre a modificar: ")
        nou_titol = input("Nou títol (deixar en blanc per no canviar): ").strip()
        nou_autor = input("Nou autor (deixar en blanc per no canviar): ").strip()
        if self.biblio.actualitzar_llibre(isbn, nou_titol or None, nou_autor or None):
            print("Llibre actualitzat.")
        else:
            print("Error en l'actualització.")

    def _modificar_usuari(self):
        dni = input("DNI de l'usuari a modificar: ")
        nou_nom = input("Nou nom (deixar en blanc per no canviar): ").strip()
        nou_cognoms = input("Nous cognoms (deixar en blanc per no canviar): ").strip()
        if self.biblio.actualitzar_usuari(dni, nou_nom or None, nou_cognoms or None):
            print("Usuari actualitzat.")
        else:
            print("Error en l'actualització.")

class MenuLector(MenuBase):
    def mostrar_opcions(self):
        print("\n--- MENÚ LECTOR ---")
        print("1. Llistar llibres disponibles")
        print("2. Fer préstec")
        print("3. Tornar llibre")
        print("4. Valorar llibre")
        print("5. Consultar préstecs actius")
        print("0. Sortir")

    def processar_opcio(self, opcio):
        if opcio == "1":
            llibres = self.biblio.llistar_llibres()
            for llibre in llibres:
                estat = "Disponible" if llibre[3] == '0' else f"Prestat a {llibre[3]}"
                print(f"{llibre[0]} - {llibre[1]} | {estat}")
        elif opcio == "2":
            isbn = input("ISBN del llibre: ")
            print(self.biblio.prestar_llibre(isbn, self.usuari['dni']))
        elif opcio == "3":
            isbn = input("ISBN a tornar: ")
            print(self.biblio.tornar_llibre(isbn))
        elif opcio == "4":
            isbn = input("ISBN del llibre: ")
            puntuacio = int(input("Puntuació (1-5): "))
            print(self.biblio.valorar_llibre(isbn, self.usuari['dni'], puntuacio))
        elif opcio == "5":
            self._veure_prestecs()

    def _veure_prestecs(self):
        cursor = self.biblio.conn.cursor()
        cursor.execute('''
            SELECT isbn, titol, data_prestec 
            FROM llibres 
            WHERE dni_prestec = ?
        ''', (self.usuari['dni'],))
        prestecs = cursor.fetchall()
        if prestecs:
            for p in prestecs:
                print(f"{p[0]} - {p[1]} | Prestat el {p[2]}")
        else:
            print("No tens préstecs actius.")