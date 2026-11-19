from typing import Tuple, Any

class Venta:
    """Clase que representa la tercera tabla relacionada: Ventas/Facturas."""
    
    def __init__(self, id_venta: int | None, id_cliente: int, id_producto: int, cantidad: int, fecha: str, total: float):
        self.__id_venta = id_venta
        self.__id_cliente = id_cliente
        self.__id_producto = id_producto
        self.__cantidad = cantidad
        self.__fecha = fecha
        self.__total = float(total)

    @property
    def id_venta(self) -> int | None:
        return self.__id_venta

    @property
    def id_cliente(self) -> int:
        return self.__id_cliente

    @property
    def id_producto(self) -> int:
        return self.__id_producto

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def fecha(self) -> str:
        return self.__fecha

    @property
    def total(self) -> float:
        return self.__total

    @classmethod
    def desde_tupla(cls, tupla: Tuple[Any, ...]) -> 'Venta':
        return cls(id_venta=tupla[0], id_cliente=tupla[1], id_producto=tupla[2], cantidad=tupla[3], fecha=tupla[4], total=tupla[5])

    def __str__(self) -> str:
        return f"Factura #{self.__id_venta} - Cliente ID: {self.__id_cliente} - Total: ${self.__total:,.2f}"