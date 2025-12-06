from src.core.security import Security
from src.roleManager.role import Role
from src.userManager.user import User
from src.tokenManager.token_service import TokenManager
from src.decorators.auth_decorators import login_required,has_role


@login_required
def ver_dashboard_admin(token):
    print("Dashboard Admin")


def main():
    password_real = "qwe"
    rounds = 14
    print(f"Contraseña Original {password_real}")
    hashed_password = Security.hash_password(password_real, rounds)
    print(f"Contraseña haseada {hashed_password}")

    print("Verificando Credenciales")
    password_is_valid = Security.verify_password("asdasd", hashed_password)
    print(password_is_valid)

    rol_admin = Role(name="Admin")
    rol_admin.add_permission("borrar_usuarios")

    usuario_nuevo = User(
        id=1, email="Bernardodoeta", password="123456", userName="bernardo"
    )
    usuario_nuevo.add_role(rol_admin.name)

    datos_usuario = {
        "id": usuario_nuevo.id,
        "username": usuario_nuevo.userName,
        "roles": usuario_nuevo.roles,
    }
    generar_token = TokenManager.crear_token(datos_usuario)
    token = generar_token

    print(token)

    comprobar_token = TokenManager.decode_token(token)
    print(comprobar_token)

    ver_dashboard_admin(token)

    @login_required
    @has_role("Admin")
    def funcion_super_secreta(token):
        print("🚀 ¡ÉXITO! Has entrado a la zona de Admin.")

    # 2. Definimos otra que requiere un rol que NO tenemos
    @login_required
    @has_role("SuperDios")
    def funcion_imposible(token):
        print("Esto no debería imprimirse nunca.")

    print("\n--- Probando acceso Admin (Debería funcionar) ---")
    try:
        funcion_super_secreta(token=token)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

    print("\n--- Probando acceso prohibido (Debería fallar) ---")
    try:
        funcion_imposible(token=token)
    except PermissionError as e:
        print(f"✅ ¡Correcto! El sistema bloqueó el acceso: {e}")
    except Exception as e:
        print(f"❌ Error diferente al esperado: {e}")
        
        
if __name__ == "__main__":
    main()
