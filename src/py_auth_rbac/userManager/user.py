from typing import List


class User:
    def __init__(self, id: int, userName: str, password: str, email: str):
        self.id = id
        self.userName = userName
        self.password = password
        self.email = email
        self.roles: List[str] = []

    def add_role(self, role_name: str):
        if role_name not in self.roles:
            self.roles.append(role_name)
        print(f"Rol Agregado {self.roles}")

    def has_role(self, role_name: str) -> bool:
        return role_name in self.roles
