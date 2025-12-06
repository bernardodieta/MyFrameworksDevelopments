from abc import ABC, abstractmethod
from typing import Optional, Any

class UserProvider(ABC):
    """
    Interfaz que debe implementar el usuario de la librería para conectar
    su base de datos con nuestro sistema de autenticación.
    """

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[Any]:
        """
        Busca un usuario por su nombre de usuario.
        Debe devolver una instancia de la clase User o None si no existe.
        """
        pass

    @abstractmethod
    def create_user(self, user_data: dict) -> Any:
        """
        Guarda un nuevo usuario en la base de datos.
        Recibe un diccionario con los datos y debe devolver el usuario creado.
        """
        pass

    @abstractmethod
    def assign_role(self, user_id: Any, role_name: str) -> bool:
        """
        Asigna un rol existente a un usuario en la base de datos.
        Debe devolver True si la operación fue exitosa.
        """
        pass
