import sys
import os

# Esto es solo para que funcione el ejemplo sin instalar la librería si estás en la carpeta raíz
# En un proyecto real, esto no es necesario si has hecho 'pip install py_auth_rbac'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from typing import Optional, Any, Dict
from py_auth_rbac.core.security import Security
from py_auth_rbac.tokenManager.token_service import TokenManager
from py_auth_rbac.userManager.user import User
from py_auth_rbac.interfaces.user_provider import UserProvider
from py_auth_rbac.decorators.auth_decorators import login_required, has_role

# --- 1. Implementación del Proveedor de Datos (Simulando una BD) ---
class InMemoryDB(UserProvider):
    """
    Esta clase simula una base de datos en memoria.
    En un caso real, aquí usarías SQL Alchemy, Django ORM, PyMongo, etc.
    """
    def __init__(self):
        self.users_db: Dict[str, User] = {} # Simula la tabla de usuarios

    def get_user_by_username(self, userName: str) -> Optional[User]:
        return self.users_db.get(userName)

    def create_user(self, user_data: dict) -> User:
        # Simulamos un ID autoincremental
        new_id = len(self.users_db) + 1
        
        new_user = User(
            id=new_id,
            userName=user_data['username'],
            password=user_data['password'], # Aquí ya debería llegar hasheada
            email=user_data['email']
        )
        
        # Guardamos en nuestro diccionario "BD"
        self.users_db[new_user.userName] = new_user
        print(f"💾 [BD] Usuario '{new_user.userName}' guardado con ID {new_user.id}")
        return new_user

    def assign_role(self, user_id: int, role_name: str) -> bool:
        # Buscamos al usuario por ID (ineficiente en dict, pero sirve para el ejemplo)
        for user in self.users_db.values():
            if user.id == user_id:
                user.add_role(role_name)
                print(f"💾 [BD] Rol '{role_name}' asignado al usuario {user.userName}")
                return True
        return False

# --- 2. Funciones Protegidas (La API de tu aplicación) ---

@login_required
def ver_perfil(token):
    # Decodificamos para saber quién es
    data = TokenManager.decode_token(token)
    print(f"👤 Perfil del usuario: {data.get('username')} (ID: {data.get('id')})")

@login_required
@has_role("Admin")
def panel_administrador(token):
    print("⚙️  Bienvenido al Panel de Administración. Tienes el poder.")

@login_required
@has_role("SuperAdmin")
def boton_nuclear(token):
    print("☢️  LANZANDO MISILES... (Esto no debería pasar)")

# --- 3. Script Principal de Prueba ---
def main():
    print("--- INICIANDO DEMO DE PY_AUTH_RBAC ---\n")
    
    # A. Inicializamos la "Base de Datos"
    db = InMemoryDB()
    
    # B. REGISTRO DE USUARIO
    print("1️⃣  Registrando usuario 'bernardo'...")
    password_plana = "mi_password_seguro"
    password_hash = Security.hash_password(password_plana)
    
    usuario = db.create_user({
        "username": "bernardo",
        "password": password_hash,
        "email": "bernardo@example.com"
    })
    
    # C. ASIGNACIÓN DE ROLES
    print("\n2️⃣  Asignando rol de Admin...")
    db.assign_role(usuario.id, "Admin")
    
    # D. LOGIN (Simulado)
    print("\n3️⃣  Intentando Login...")
    # Buscamos usuario
    user_found = db.get_user_by_username("bernardo")
    
    if user_found and Security.verify_password("mi_password_seguro", user_found.password):
        print("✅ Login Correcto!")
        
        # Generamos el Token
        token_data = {
            "id": user_found.id,
            "username": user_found.userName,
            "roles": user_found.roles
        }
        token = TokenManager.crear_token(token_data)
        print(f"🔑 Token Generado: {token[:20]}... (truncado)")
    else:
        print("❌ Login Fallido")
        return

    # E. PROBANDO ACCESOS
    print("\n4️⃣  Probando accesos protegidos...")
    
    print("\n> Intentando ver perfil (Requiere Login):")
    try:
        ver_perfil(token=token)
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n> Intentando entrar al Panel Admin (Requiere Rol Admin):")
    try:
        panel_administrador(token=token)
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n> Intentando tocar Botón Nuclear (Requiere Rol SuperAdmin):")
    try:
        boton_nuclear(token=token)
    except PermissionError as e:
        print(f"🛡️  BLOQUEADO CORRECTAMENTE: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
