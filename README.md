# 📚 Biblioteca Digital amb SQLite3

Aquest projecte és una biblioteca digital desenvolupada en Python que permet gestionar llibres, préstecs i usuaris mitjançant una base de dades SQLite3. Inclou control d'accés per a **administradors** i **lectors**, validació de dades i gestió de restriccions.

---

## 🔐 Accés Ràpid per a Proves

Pots utilitzar aquests usuaris per provar l’aplicació:

* **Administrador**

  * 🆔 DNI: `admin`
  * 🔑 Contrasenya: `admin123`
  * 🎯 Accés complet a totes les funcionalitats

* **Lector Predefinit**

  * 🆔 DNI: `11`
  * 🔑 Contrasenya: `11`
  * ℹ️ *Aquest lector s’ha afegit directament a la base de dades per facilitar proves. El sistema estàndard requereix DNIs en format `8 dígits + lletra`, per tant, no es poden crear DNIs curts com “11”.*

---

## 🚀 Funcionalitats Principals

### 📖 Gestió de Llibres

* Afegir, editar i eliminar llibres (ISBN, títol, autor)
* Gestionar préstecs amb restriccions:

  * Màxim **3 llibres** per usuari
  * Préstec màxim de **30 dies**
* Valorar llibres (de **1 a 5 estrelles**)
* Llistat amb estat de disponibilitat

### 👤 Gestió d'Usuaris

* Registre de nous usuaris amb **contrasenya xifrada (SHA-256)**
* Promoció de lectors a administradors
* Validació de **DNI** amb format `12345678A`

### ⚙️ Altres Característiques

* Creació automàtica de taules SQLite3
* Menús diferenciats per rols (*admin* i *lector*)
* Gestió d'errors i missatges descriptius

---

## 📂 Estructura de la Base de Dades

### `usuaris`

| DNI (PK) | Nom | Cognoms | Contrasenya (SHA-256) | Tipus (`admin` / `lector`) |
| -------- | --- | ------- | --------------------- | -------------------------- |

### `llibres`

| ISBN (PK)                                            | Títol | Autor | DNI Préstec | Data Préstec |
| ---------------------------------------------------- | ----- | ----- | ----------- | ------------ |
| *Si `dni_prestec = "0"`, el llibre està disponible.* |       |       |             |              |

### `valoracions`

| ID (PK) | ISBN | DNI | Puntuació (1-5) |
| ------- | ---- | --- | --------------- |

---

### 📋 Menús Disponibles

**Menú Administrador**

* Gestionar usuaris i llibres
* Modificar dades
* Veure tots els registres

**Menú Lector**

* Fer i retornar préstecs
* Valorar llibres
* Consultar préstecs actius

---

## 🧪 Tests i Validació

Executa els tests unitaris per verificar funcionalitats:

```bash
python test_llibre.py     # Proves de la classe Llibre
python test_pt1.py        # Proves de préstecs i usuaris
```

---

## 🛠️ Millores Previstes

* Validació completa de DNI amb lletra segons algorisme oficial
* Interfície gràfica amb Tkinter o PyQt
* Exportació de dades en formats CSV/JSON
* API REST per a accés remot

---

## 👤 Autor

Projecte desenvolupat per **Cesc** · 2025
📁 [GitHub](https://github.com/cmoleroce/M0487_RA56_v3_Molero.git)
