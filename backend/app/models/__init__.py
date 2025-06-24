# Importações dos modelos principais
from .user import User, Genero, NivelAtividade, ObjetivoFitness
from .training import Treino, TemplateTreino, ExercicioTemplate, StatusTreino, CategoriaTreino
from .exercise import Exercicio, ComPeso, SemPeso, HistoricoExecucao, GrupoMuscular, Dificuldade, TipoExercicio

__all__ = [
    "User",
    "Genero", 
    "NivelAtividade",
    "ObjetivoFitness",
    "Treino",
    "TemplateTreino",
    "ExercicioTemplate", 
    "StatusTreino",
    "CategoriaTreino",
    "Exercicio",
    "ComPeso", 
    "SemPeso",
    "HistoricoExecucao",
    "GrupoMuscular",
    "Dificuldade",
    "TipoExercicio"
] 