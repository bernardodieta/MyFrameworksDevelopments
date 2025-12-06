from typing import List


class Role:
    def __init__(self, name: str):
        self.name = name
        self.permissions: List[str] = []

    def add_permission(self, permission: str):
        if permission not in self.permissions:
            self.permissions.append(permission)
            print(f"Permission Agregado {permission}")

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions
