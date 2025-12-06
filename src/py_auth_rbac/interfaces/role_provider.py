from abc import ABC, abstractmethod
from typing import Optional, Any, List

class RoleProvider(ABC):
    """
    Interfaz para gestionar la persistencia de los Roles.
    """

    @abstractmethod
    def get_role_by_name(self, name: str) -> Optional[Any]:
        """
        Busca un rol por su nombre.
        """
        pass

    @abstractmethod
    def create_role(self, name: str, permissions: List[str] = []) -> Any:
        """
        Crea un nuevo rol en la base de datos con una lista de permisos opcional.
        """
        pass
