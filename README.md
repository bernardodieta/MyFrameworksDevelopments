# Python Auth Library

LIbreria liguera y modular para manejar Autenticación (JWT) y Autorización basada en Roles (RBAC) en Python. Diseñado para ser agnóstico a la base de datos.

## Características

*   **Seguridad**: Hashing de contraseñas con `bcrypt`.
*   **Tokens**: Generación y validación de JSON Web Tokens (JWT).
*   **RBAC**: Gestión de Usuarios, Roles y Permisos.
*   **Decoradores**: `@login_required` y `@has_role` para proteger tus funciones.
*   **Flexible**: Usa interfaces para conectar con CUALQUIER base de datos (SQL, NoSQL, JSON, Memoria).

## 📦 Instalación

1.  Clona este repositorio o copia la carpeta `src` en tu proyecto.
2.  Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Cómo usarlo

### 1. Implementa los Proveedores de Datos (Interfaces)

Como el framework no sabe qué base de datos usas, debes crear una clase que conecte el framework con tus datos implementando `UserProvider`.

```python
# mi_adaptador_db.py
from src.interfaces.user_provider import UserProvider
from src.userManager.user import User

# Ejemplo simulando una base de datos en memoria
class InMemoryDB(UserProvider):
    def __init__(self):
        self.users_db = []

    def get_user_by_username(self, username: str):
        for user in self.users_db:
            if user.username == username:
                return user
        return None

    def create_user(self, user_data: dict):
        new_user = User(
            id=len(self.users_db) + 1,
            username=user_data['username'],
            password=user_data['password'], # Recuerda pasar el hash, no el texto plano
            email=user_data['email']
        )
        self.users_db.append(new_user)
        return new_user

    def assign_role(self, user_id, role_name):
        # Lógica para guardar la relación en tu BD
        for user in self.users_db:
            if user.id == user_id:
                user.add_role(role_name)
                return True
        return False
```

### 2. Inicializa y Crea Usuarios

```python
from src.core.security import Security
from src.tokenManager.token_service import TokenManager

# 1. Instancia tu adaptador
db_adapter = InMemoryDB()

# 2. Crea un usuario (Recuerda hashear la contraseña antes)
password_hash = Security.hash_password("mi_secreto")
usuario = db_adapter.create_user({
    "username": "admin",
    "password": password_hash,
    "email": "admin@test.com"
})

# 3. Asigna roles
db_adapter.assign_role(usuario.id, "Admin")
```

### 3. Genera un Token (Login)

```python
# Datos que irán en el token
datos_token = {
    "id": usuario.id,
    "username": usuario.username,
    "roles": usuario.roles
}

token_jwt = TokenManager.crear_token(datos_token)
print(f"Tu token es: {token_jwt}")
```

### 4. Protege tus Funciones

Usa los decoradores para asegurar tus rutas o funciones.

```python
from src.decorators.auth_decorators import login_required, has_role

@login_required
@has_role("Admin")
def borrar_base_de_datos(token):
    print("⚠️ Borrando base de datos...")

# Llamada (Simulando que recibes el token del frontend)
try:
    borrar_base_de_datos(token=token_jwt)
except PermissionError as e:
    print(f"Acceso denegado: {e}")
```

## Estructura del Proyecto

*   `src/core`: Utilidades de criptografía.
*   `src/decorators`: Lógica de protección (`@login_required`).
*   `src/interfaces`: Contratos que debes implementar para conectar tu BD.
*   `src/tokenManager`: Manejo de JWT.
*   `src/userManager`: Modelos de usuario.
*   `src/roleManager`: Modelos de roles.
