import numpy as np
import nashpy as nash
from typing import List, Tuple

def compute_nash_equilibrium(A: List[List[float]], B: List[List[float]]) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Вычисляет все равновесия Нэша в смешанных стратегиях для биматричной игры.
    Возвращает список кортежей (стратегия_игрока1, стратегия_игрока2).
    """
    game = nash.Game(np.array(A), np.array(B))
    equilibria = list(game.support_enumeration())
    return equilibria