from functools import wraps
from ..tokenManager.token_service import TokenManager
import inspect


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        token = bound_args.arguments.get("token")

        if not token:
            raise PermissionError("Acceso denegado! se requiere un token.")

        try:
            payload = TokenManager.decode_token(token)
            print(f"Accesp autorizado para: {payload.get('username')}")

            return func(*args, **kwargs)
        except Exception as e:
            raise PermissionError(f"Token Invalido o expirado: {str(e)}")

    return wrapper


def has_role(required_role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            token = bound_args.arguments.get("token")
            payload = TokenManager.decode_token(token)
            roles_usuario = payload.get("roles", [])
            if required_role not in roles_usuario:
                raise PermissionError(f"Se requiere el rol de {required_role}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
