from typing import Tuple, Any

class Producto:
    """Clase que representa un producto de tecnología (Computadores, Impresoras, Mouse, Celulares)."""
    
    def __init__(self, id_producto: int | None, nombre: str, categoria: str, precio: float, stock: int):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__categoria = categoria
        self.__precio = float(precio)
        self.__stock = int(stock)

    @property
    def id_producto(self) -> int | None:
        return self.__id_producto

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def categoria(self) -> str:
        return self.__categoria

    @property
    def precio(self) -> float:
        return self.__precio

    @property
    def stock(self) -> int:
        return self.__stock

    @classmethod
    def desde_tupla(cls, tupla: Tuple[Any, ...]) -> 'Producto':
        """Método de fábrica para instanciar un Producto desde SQLite."""
        return cls(id_producto=tupla[0], nombre=tupla[1], categoria=tupla[2], precio=tupla[3], stock=tupla[4])

    def __str__(self) -> str:
        return f"[{self.__categoria}] {self.__nombre} - ${self.__precio:,.2f} (Stock: {self.__stock})"

    def __len__(self) -> int:
        """Método mágico __len__ que retorna el stock disponible del producto."""
        return self.__stock

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Producto):
            return False
        return self.__id_producto == otro.__id_producto