import bcrypt


class Security:
    @staticmethod
    def hash_password(password: str, rounds: int = 12) -> str:
        if password == "":
            return "la contraseña no puede ser un campo vacio"
        if rounds:
            print(f"Rounds recibido: {rounds}")

        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:

        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
