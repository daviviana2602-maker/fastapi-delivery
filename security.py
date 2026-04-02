from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")   # criptografia com argon2 (não tem limite de bytes)