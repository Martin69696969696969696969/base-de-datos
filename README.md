📚 Sistema de Biblioteca en Python y MySQL

Este proyecto implementa un sistema de gestión de biblioteca utilizando Python y MySQL.
Permite administrar libros, usuarios y préstamos a través de una interfaz de consola interactiva, aplicando los principios de Programación Orientada a Objetos (POO) y manejo de base de datos con el módulo mysql.connector.

🧩 Características principales

✅ Conexión a una base de datos MySQL
✅ Registro, búsqueda y listado de libros
✅ Registro, búsqueda y listado de usuarios
✅ Registro, listado y devolución de préstamos
✅ Validación de datos y manejo de errores
✅ Registro de eventos mediante logging (biblioteca.log)
✅ Diseño modular y orientado a objetos (POO)

⚙️ Requisitos

Python 3.8+

MySQL Server

Módulo mysql-connector-python

Instala el conector ejecutando:

pip install mysql-connector-python

🗄️ Estructura de la base de datos

Ejecuta en MySQL los siguientes comandos para crear la base de datos y sus tablas:

CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    anio INT NOT NULL,
    disponible BOOLEAN DEFAULT TRUE
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('estudiante', 'profesor', 'administrador') NOT NULL
);

CREATE TABLE prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_libro INT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_libro) REFERENCES libros(id)
);

🚀 Ejecución del programa

Clona o descarga el repositorio.

Asegúrate de tener corriendo tu servidor MySQL.

Modifica los datos de conexión en la clase ConexionBD (usuario, contraseña, host, base de datos).

Ejecuta el programa:

python biblioteca.py

🧠 Uso del menú

El programa se ejecuta en la terminal con un menú interactivo dividido en tres secciones:

Menú principal
1. Libros
2. Usuarios
3. Préstamos
4. Salir

Gestión de Libros

Registrar un nuevo libro

Listar todos los libros

Buscar libros por título

Gestión de Usuarios

Registrar nuevo usuario

Listar todos los usuarios

Buscar usuarios por nombre

Gestión de Préstamos

Registrar préstamo de un libro

Listar préstamos actuales y pasados

Devolver libro (actualiza disponibilidad y fecha de devolución)

🧱 Clases principales (POO)
Clase	Responsabilidad	Conceptos POO
ConexionBD	Maneja la conexión y ejecución de queries a MySQL	Encapsulamiento, manejo de errores
Libro	Representa un libro con título, autor, año y disponibilidad	Encapsulamiento, validación
Usuario	Representa un usuario con nombre y tipo (estudiante, profesor, administrador)	Encapsulamiento
Prestamo	Modela el préstamo de un libro a un usuario	Composición, validación
SistemaBiblioteca	Coordina la interacción entre todas las clases y el usuario	Abstracción, polimorfismo funcional
🪵 Logging

Todas las operaciones se registran en el archivo biblioteca.log con formato:

2025-10-15 10:20:31,554 - INFO - Conexión establecida.
2025-10-15 10:21:10,402 - INFO - Libro ID 1: El Quijote
2025-10-15 10:21:35,901 - INFO - Préstamo ID 3


Esto permite llevar un historial de eventos importantes, errores y operaciones.

🧪 Datos de prueba

Puedes insertar algunos datos automáticamente descomentando la función al final del código:

if __name__ == "__main__":
    sistema = SistemaBiblioteca()
    insertar_datos_prueba(sistema)
    sistema.menu()


Esto agregará libros, usuarios y un préstamo inicial para pruebas.

🧩 Principios POO aplicados

Encapsulamiento: Uso de atributos privados (__atributo) con métodos get_ y set_.

Abstracción: Clases representan entidades reales (Libro, Usuario, Prestamo).

Composición: SistemaBiblioteca usa objetos de otras clases para funcionar.

Modularidad: Cada clase tiene responsabilidades bien definidas.

Polimorfismo (parcial): Uso uniforme de métodos get/set y menu_ en distintas entidades.

💡 Mejoras futuras

Implementar interfaz gráfica con Tkinter o PyQt.

Agregar autenticación de usuarios.

Exportar reportes en CSV o PDF.

Crear API REST con Flask o FastAPI.

Controlar multas o fechas límite de devolución.

✍️ Autor

Desarrollado por [Tu Nombre]
Proyecto educativo — Gestión de Biblioteca en Python y MySQL.# base-de-datos
base de datos

<img width="1652" height="709" alt="image" src="https://github.com/user-attachments/assets/c3f3eee4-20f5-4b32-8d29-bf4656be24ec" />

