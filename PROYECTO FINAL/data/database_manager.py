import sqlite3
from typing import Generator
from contextlib import contextmanager

class DatabaseManager:
    """Gestor de base de datos con patrón Context Manager y control de transacciones."""
    
    def __init__(self, nombre_db: str = "tienda_computo.db"):
        self.__nombre_db = nombre_db
        self.inicializar_base_datos()

    @contextmanager
    def obtener_conexion(self) -> Generator[sqlite3.Connection, None, None]:
        """Gestor de contexto with para manejar conexiones, commit, rollback y cierre automático."""
        conexion = sqlite3.connect(self.__nombre_db)
        # Integridad referencial obligatoria requerida por la rúbrica
        conexion.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conexion
            conexion.commit()
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()

    def inicializar_base_datos(self) -> None:
        """Crea las 3 tablas relacionales obligatorias: clientes, productos y ventas."""
        with self.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    precio REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_cliente INTEGER NOT NULL,
                    id_producto INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    total REAL NOT NULL,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
                    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE CASCADE
                )
            """)