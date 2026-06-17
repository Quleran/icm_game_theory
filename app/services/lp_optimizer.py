import pulp
import numpy as np
from typing import List, Dict, Optional

def optimize_margin(A: List[List[float]], B: List[List[float]]) -> Optional[Dict]:
    """
    Решает задачу линейного программирования для максимизации минимальной маржи m.

    :param A: матрица выигрышей игрока 1
    :param B: матрица выигрышей игрока 2
    :return: словарь с ключами 'margin', 'strategy_a', 'strategy_b' или None в случае ошибки
    """
    n = len(A)  # число чистых стратегий

    # Создаём задачу максимизации
    prob = pulp.LpProblem("Maximize_Margin", pulp.LpMaximize)

    # Переменная m (маржа) – неотрицательная
    m = pulp.LpVariable("m", lowBound=0)

    # Переменные стратегий x_i, y_j
    x = [pulp.LpVariable(f"x_{i}", lowBound=0) for i in range(n)]
    y = [pulp.LpVariable(f"y_{j}", lowBound=0) for j in range(n)]

    # Целевая функция: максимизировать m
    prob += m

    # Ограничения: суммы вероятностей = 1
    prob += pulp.lpSum(x) == 1
    prob += pulp.lpSum(y) == 1

    # Ограничения для игрока 1: для каждой чистой стратегии i, ожидаемая прибыль >= m
    for i in range(n):
        prob += pulp.lpSum(A[i][j] * y[j] for j in range(n)) >= m

    # Ограничения для игрока 2: для каждой чистой стратегии j, ожидаемая прибыль >= m
    for j in range(n):
        prob += pulp.lpSum(B[i][j] * x[i] for i in range(n)) >= m

    # Решаем задачу (по умолчанию используется симплекс-метод)
    prob.solve(pulp.PULP_CBC_CMD(msg=0))  # msg=0 отключает вывод

    # Проверяем статус
    if prob.status != pulp.LpStatusOptimal:
        return None

    # Извлекаем значения
    margin_opt = pulp.value(m)
    strategy_a = [pulp.value(x[i]) for i in range(n)]
    strategy_b = [pulp.value(y[j]) for j in range(n)]

    return {
        "margin": margin_opt,
        "strategy_a": strategy_a,
        "strategy_b": strategy_b
    }