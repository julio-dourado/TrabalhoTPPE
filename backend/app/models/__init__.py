# Importações dos modelos principais
from .user import User
from .training import Treino
from .exercise import Exercicio, ComPeso, SemPeso

__all__ = [
    "User",
    "Treino", 
    "Exercicio",
    "ComPeso", 
    "SemPeso"
] 