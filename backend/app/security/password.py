from passlib.context import CryptContext

# Define o contexto de hash para senhas
# Usa bcrypt como algoritmo padrão, o que é seguro para armazenamento de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde a um hash de senha.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_senha_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano.
    """
    return pwd_context.hash(password)

