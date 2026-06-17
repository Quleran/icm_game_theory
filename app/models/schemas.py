from typing import List
from pydantic import BaseModel, Field

class GameRequest(BaseModel):
    payoff_matrix_a: List[List[float]] = Field(..., description="Матрица прибыли игрока 1")
    payoff_matrix_b: List[List[float]] = Field(..., description="Матрица прибыли игрока 2")

class Equilibrium(BaseModel):
    strategy_a: List[float] = Field(..., description="Смешанная стратегия игрока 1 (вероятности)")
    strategy_b: List[float] = Field(..., description="Смешанная стратегия игрока 2 (вероятности)")

class GameResponse(BaseModel):
    equilibria: List[Equilibrium] = Field(..., description="Список найденных равновесий")

class OptimizationRequest(BaseModel):
    payoff_matrix_a: List[List[float]] = Field(..., description="Матрица прибыли игрока 1")
    payoff_matrix_b: List[List[float]] = Field(..., description="Матрица прибыли игрока 2")

class OptimizationResponse(BaseModel):
    optimal_margin: float = Field(..., description="Максимальная гарантированная маржа (m)")
    strategy_a: List[float] = Field(..., description="Оптимальная стратегия игрока 1")
    strategy_b: List[float] = Field(..., description="Оптимальная стратегия игрока 2")