from typing import Tuple, Any

class Cliente:
    """Clase que representa a un cliente de la tienda de cómputo."""
    
    def __init__(self, id_cliente: int | None, nombre: str, telefono: str, email: str):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__telefono = telefono
        self.__email = email

    @property
    def id_cliente(self) -> int | None:
        return self.__id_cliente

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def telefono(self) -> str:
        return self.__telefono

    @property
    def email(self) -> str:
        return self.__email

    @classmethod
    def desde_tupla(cls, tupla: Tuple[Any, ...]) -> 'Cliente':
        """Método de fábrica para instanciar un Cliente desde una tupla de SQLite."""
        return cls(id_cliente=tupla[0], nombre=tupla[1], telefono=tupla[2], email=tupla[3])

    def __str__(self) -> str:
        return f"Cliente(ID: {self.__id_cliente}, Nombre: {self.__nombre}, Teléfono: {self.__telefono})"

    def __repr__(self) -> str:
        return f"Cliente({self.__id_cliente}, '{self.__nombre}', '{self.__telefono}', '{self.__email}')"

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Cliente):
            return False
        return self.__id_cliente == otro.__id_cliente