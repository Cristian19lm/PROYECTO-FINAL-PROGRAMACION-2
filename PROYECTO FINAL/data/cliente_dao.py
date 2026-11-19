from typing import List
from data.database_manager import DatabaseManager
from domain.cliente import Cliente

class ClienteDAO:
    """Patrón DAO para operaciones CRUD sobre la tabla clientes."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.__db_manager = db_manager

    def insertar(self, cliente: Cliente) -> None:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono, email) VALUES (?, ?, ?)",
                (cliente.nombre, cliente.telefono, cliente.email)
            )

    def obtener_todos(self) -> List[Cliente]:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_cliente, nombre, telefono, email FROM clientes")
            return [Cliente.desde_tupla(row) for row in cursor.fetchall()]

    def actualizar(self, cliente: Cliente) -> None:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE clientes SET nombre = ?, telefono = ?, email = ? WHERE id_cliente = ?",
                (cliente.nombre, cliente.telefono, cliente.email, cliente.id_cliente)
            )

    def eliminar(self, id_cliente: int) -> None:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = ?", (id_cliente,))