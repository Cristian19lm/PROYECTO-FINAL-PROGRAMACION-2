from typing import List
from data.database_manager import DatabaseManager
from domain.producto import Producto
from domain.venta import Venta

class ProductoRepository:
    """Patrón Repository para la gestión de productos y registro de ventas."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.__db_manager = db_manager

    def insertar_producto(self, producto: Producto) -> None:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
                (producto.nombre, producto.categoria, producto.precio, producto.stock)
            )

    def obtener_productos(self) -> List[Producto]:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos")
            return [Producto.desde_tupla(row) for row in cursor.fetchall()]

    def actualizar_producto(self, producto: Producto) -> None:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE productos SET nombre = ?, categoria = ?, precio = ?, stock = ? WHERE id_producto = ?",
                (producto.nombre, producto.categoria, producto.precio, producto.stock, producto.id_producto)
            )

    def eliminar_producto(self, id_producto: int) -> None:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))

    def registrar_venta(self, venta: Venta) -> bool:
        """Registra una venta y descuenta automáticamente el stock del producto de forma transaccional."""
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT stock FROM productos WHERE id_producto = ?", (venta.id_producto,))
            resultado = cursor.fetchone()
            if not resultado or resultado[0] < venta.cantidad:
                return False  
            
            nuevo_stock = resultado[0] - venta.cantidad
            cursor.execute("UPDATE productos SET stock = ? WHERE id_producto = ?", (nuevo_stock, venta.id_producto))
            
            cursor.execute(
                "INSERT INTO ventas (id_cliente, id_producto, cantidad, fecha, total) VALUES (?, ?, ?, ?, ?)",
                (venta.id_cliente, venta.id_producto, venta.cantidad, venta.fecha, venta.total)
            )
            return True

    def obtener_ventas(self) -> List[Venta]:
        with self.__db_manager.obtener_conexion() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_venta, id_cliente, id_producto, cantidad, fecha, total FROM ventas")
            return [Venta.desde_tupla(row) for row in cursor.fetchall()]