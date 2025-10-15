import mysql.connector
from mysql.connector import Error
from datetime import date
import logging

logging.basicConfig(filename='biblioteca.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConexionBD:
    def __init__(self):
        self.conexion = None
        try:
            self.conexion = mysql.connector.connect(host="localhost", user="root", password="toor", database="biblioteca", auth_plugin='mysql_native_password')
            if self.conexion.is_connected():
                logging.info("Conexión establecida.")
                print("Conexión OK.")
        except Error as e:
            logging.error(f"Error conexión: {e}")
            print(f"Error: {e}")

    def ejecutar_query(self, query, params=None):
        cursor = self.conexion.cursor()
        try:
            if params: cursor.execute(query, params)
            else: cursor.execute(query)
            self.conexion.commit()
            logging.info(f"Query OK: {query}")
            return cursor
        except Error as e:
            self.conexion.rollback()
            logging.error(f"Error query: {e}")
            print(f"Error: {e}")
            return None

    def fetch_all(self, query, params=None):
        cursor = self.conexion.cursor()
        try:
            if params: cursor.execute(query, params)
            else: cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            logging.error(f"Error fetch_all: {e}")
            return []
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self.conexion.cursor()
        try:
            if params: cursor.execute(query, params)
            else: cursor.execute(query)
            return cursor.fetchone()
        except Error as e:
            logging.error(f"Error fetch_one: {e}")
            return None
        finally:
            cursor.close()

    def close(self):
        if self.conexion and self.conexion.is_connected():
            self.conexion.close()
            logging.info("Conexión cerrada.")

class Libro:
    def __init__(self, titulo="", autor="", anio=0, disponible=True):
        self.__titulo = titulo
        self.__autor = autor
        self.__anio = anio
        self.__disponible = disponible
        self.__id = None

    def get_id(self): return self.__id
    def get_titulo(self): return self.__titulo
    def get_autor(self): return self.__autor
    def get_anio(self): return self.__anio
    def get_disponible(self): return self.__disponible

    def set_id(self, id_val): self.__id = id_val
    def set_titulo(self, titulo):
        if titulo.strip(): self.__titulo = titulo.strip()
        else: raise ValueError("Título vacío.")
    def set_autor(self, autor):
        if autor.strip(): self.__autor = autor.strip()
        else: raise ValueError("Autor vacío.")
    def set_anio(self, anio):
        if isinstance(anio, int) and anio > 0: self.__anio = anio
        else: raise ValueError("Año inválido.")
    def set_disponible(self, disponible):
        if isinstance(disponible, bool): self.__disponible = disponible
        else: raise ValueError("Disponible inválido.")

class Usuario:
    def __init__(self, nombre="", tipo="estudiante"):
        self.__nombre = nombre
        self.__tipo = tipo
        self.__id = None

    def get_id(self): return self.__id
    def get_nombre(self): return self.__nombre
    def get_tipo(self): return self.__tipo

    def set_id(self, id_val): self.__id = id_val
    def set_nombre(self, nombre):
        if nombre.strip(): self.__nombre = nombre.strip()
        else: raise ValueError("Nombre vacío.")
    def set_tipo(self, tipo):
        tipos = ["estudiante", "profesor", "administrador"]
        if tipo.lower() in tipos: self.__tipo = tipo.lower()
        else: raise ValueError(f"Tipo inválido: {tipos}")

class Prestamo:
    def __init__(self, id_usuario=0, id_libro=0, fecha_prestamo=None, fecha_devolucion=None):
        self.__id_usuario = id_usuario
        self.__id_libro = id_libro
        self.__fecha_prestamo = fecha_prestamo or date.today()
        self.__fecha_devolucion = fecha_devolucion
        self.__id = None

    def get_id(self): return self.__id
    def get_id_usuario(self): return self.__id_usuario
    def get_id_libro(self): return self.__id_libro
    def get_fecha_prestamo(self): return self.__fecha_prestamo
    def get_fecha_devolucion(self): return self.__fecha_devolucion

    def set_id(self, id_val): self.__id = id_val
    def set_id_usuario(self, id_usuario):
        if isinstance(id_usuario, int) and id_usuario > 0: self.__id_usuario = id_usuario
        else: raise ValueError("ID usuario inválido.")
    def set_id_libro(self, id_libro):
        if isinstance(id_libro, int) and id_libro > 0: self.__id_libro = id_libro
        else: raise ValueError("ID libro inválido.")
    def set_fecha_devolucion(self, fecha): self.__fecha_devolucion = fecha

class SistemaBiblioteca:
    def __init__(self):
        self.bd = ConexionBD()

    def registrar_libro(self, libro):
        query = "INSERT INTO libros (titulo, autor, anio, disponible) VALUES (%s, %s, %s, %s)"
        params = (libro.get_titulo(), libro.get_autor(), libro.get_anio(), libro.get_disponible())
        cursor = self.bd.ejecutar_query(query, params)
        if cursor:
            libro.set_id(cursor.lastrowid)
            logging.info(f"Libro ID {libro.get_id()}: {libro.get_titulo()}")
            print(f"Libro ID {libro.get_id()}")
            return True
        return False

    def listar_libros(self):
        resultados = self.bd.fetch_all("SELECT * FROM libros ORDER BY titulo")
        if not resultados: print("Sin libros."); return
        print("ID | Título | Autor | Año | Disp.")
        for row in resultados:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {'Sí' if row[4] else 'No'}")

    def buscar_libro(self, titulo):
        params = (f"%{titulo}%",)
        resultados = self.bd.fetch_all("SELECT * FROM libros WHERE titulo LIKE %s", params)
        if not resultados: print("No encontrado."); return
        print("ID | Título | Autor | Año | Disp.")
        for row in resultados:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {'Sí' if row[4] else 'No'}")

    def actualizar_disponibilidad_libro(self, id_libro, disponible):
        params = (disponible, id_libro)
        return self.bd.ejecutar_query("UPDATE libros SET disponible = %s WHERE id = %s", params) is not None

    def registrar_usuario(self, usuario):
        query = "INSERT INTO usuarios (nombre, tipo) VALUES (%s, %s)"
        params = (usuario.get_nombre(), usuario.get_tipo())
        cursor = self.bd.ejecutar_query(query, params)
        if cursor:
            usuario.set_id(cursor.lastrowid)
            logging.info(f"Usuario ID {usuario.get_id()}: {usuario.get_nombre()}")
            print(f"Usuario ID {usuario.get_id()}")
            return True
        return False

    def listar_usuarios(self):
        resultados = self.bd.fetch_all("SELECT * FROM usuarios ORDER BY nombre")
        if not resultados: print("Sin usuarios."); return
        print("ID | Nombre | Tipo")
        for row in resultados:
            print(f"{row[0]} | {row[1]} | {row[2]}")

    def buscar_usuario(self, nombre):
        params = (f"%{nombre}%",)
        resultados = self.bd.fetch_all("SELECT * FROM usuarios WHERE nombre LIKE %s", params)
        if not resultados: print("No encontrado."); return
        print("ID | Nombre | Tipo")
        for row in resultados:
            print(f"{row[0]} | {row[1]} | {row[2]}")

    def existe_usuario(self, id_usuario):
        return self.bd.fetch_one("SELECT id FROM usuarios WHERE id = %s", (id_usuario,)) is not None

    def existe_libro(self, id_libro):
        return self.bd.fetch_one("SELECT id FROM libros WHERE id = %s", (id_libro,)) is not None

    def esta_libro_disponible(self, id_libro):
        result = self.bd.fetch_one("SELECT disponible FROM libros WHERE id = %s", (id_libro,))
        return result and result[0]

    def registrar_prestamo(self, prestamo):
        if not self.existe_usuario(prestamo.get_id_usuario()):
            print("Usuario no existe."); return False
        if not self.existe_libro(prestamo.get_id_libro()):
            print("Libro no existe."); return False
        if not self.esta_libro_disponible(prestamo.get_id_libro()):
            print("Libro no disponible."); return False
        query = "INSERT INTO prestamos (id_usuario, id_libro, fecha_prestamo, fecha_devolucion) VALUES (%s, %s, %s, %s)"
        params = (prestamo.get_id_usuario(), prestamo.get_id_libro(), prestamo.get_fecha_prestamo(), prestamo.get_fecha_devolucion())
        cursor = self.bd.ejecutar_query(query, params)
        if cursor:
            prestamo.set_id(cursor.lastrowid)
            self.actualizar_disponibilidad_libro(prestamo.get_id_libro(), False)
            logging.info(f"Préstamo ID {prestamo.get_id()}")
            print(f"Préstamo ID {prestamo.get_id()}")
            return True
        return False

    def listar_prestamos(self):
        query = """SELECT p.id, u.nombre, l.titulo, p.fecha_prestamo, p.fecha_devolucion 
                   FROM prestamos p JOIN usuarios u ON p.id_usuario = u.id 
                   JOIN libros l ON p.id_libro = l.id ORDER BY p.fecha_prestamo DESC"""
        resultados = self.bd.fetch_all(query)
        if not resultados: print("Sin préstamos."); return
        print("ID | Usuario | Libro | F. Préstamo | F. Devolución")
        for row in resultados:
            dev = row[4].strftime("%Y-%m-%d") if row[4] else "Pendiente"
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3].strftime('%Y-%m-%d')} | {dev}")

    def devolver_libro(self, id_prestamo):
        result = self.bd.fetch_one("SELECT id_libro FROM prestamos WHERE id = %s AND fecha_devolucion IS NULL", (id_prestamo,))
        if not result: print("Préstamo inválido."); return False
        id_libro = result[0]
        self.bd.ejecutar_query("UPDATE prestamos SET fecha_devolucion = %s WHERE id = %s", (date.today(), id_prestamo))
        self.actualizar_disponibilidad_libro(id_libro, True)
        logging.info(f"Devuelto préstamo {id_prestamo}")
        print("Libro devuelto.")
        return True

    def menu(self):
        while True:
            print("\n1. Libros 2. Usuarios 3. Préstamos 4. Salir")
            op = input("Opción: ").strip()
            if op == "1": self.menu_libros()
            elif op == "2": self.menu_usuarios()
            elif op == "3": self.menu_prestamos()
            elif op == "4": self.bd.close(); break
            else: print("Inválido.")

    def menu_libros(self):
        while True:
            print("\n1. Registrar 2. Listar 3. Buscar 4. Volver")
            op = input("Opción: ").strip()
            if op == "1":
                try:
                    titulo, autor, anio = input("Título: ").strip(), input("Autor: ").strip(), int(input("Año: "))
                    self.registrar_libro(Libro(titulo, autor, anio))
                except: print("Error validación.")
            elif op == "2": self.listar_libros()
            elif op == "3":
                titulo = input("Buscar: ").strip()
                if titulo: self.buscar_libro(titulo)
            elif op == "4": break
            else: print("Inválido.")

    def menu_usuarios(self):
        while True:
            print("\n1. Registrar 2. Listar 3. Buscar 4. Volver")
            op = input("Opción: ").strip()
            if op == "1":
                try:
                    nombre, tipo = input("Nombre: ").strip(), input("Tipo: ").strip().lower()
                    self.registrar_usuario(Usuario(nombre, tipo))
                except: print("Error validación.")
            elif op == "2": self.listar_usuarios()
            elif op == "3":
                nombre = input("Buscar: ").strip()
                if nombre: self.buscar_usuario(nombre)
            elif op == "4": break
            else: print("Inválido.")

    def menu_prestamos(self):
        while True:
            print("\n1. Registrar 2. Listar 3. Devolver 4. Volver")
            op = input("Opción: ").strip()
            if op == "1":
                try:
                    id_u, id_l = int(input("ID Usuario: ")), int(input("ID Libro: "))
                    self.registrar_prestamo(Prestamo(id_u, id_l))
                except: print("Error IDs.")
            elif op == "2": self.listar_prestamos()
            elif op == "3":
                try:
                    id_p = int(input("ID Préstamo: "))
                    self.devolver_libro(id_p)
                except: print("Error ID.")
            elif op == "4": break
            else: print("Inválido.")

def insertar_datos_prueba(sistema):
    libros = [Libro("El Quijote", "Cervantes", 1605), Libro("1984", "Orwell", 1949)]
    for l in libros: sistema.registrar_libro(l)
    usuarios = [Usuario("Juan", "estudiante"), Usuario("María", "profesor")]
    for u in usuarios: sistema.registrar_usuario(u)
    sistema.registrar_prestamo(Prestamo(1, 1))
    print("Datos prueba insertados.")

if __name__ == "__main__":
    sistema = SistemaBiblioteca()
    sistema.menu()
