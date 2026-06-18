import pulp
from typing import List, Dict, Optional

def optimize_margin(A: List[List[float]], B: List[List[float]]) -> Optional[Dict]:
    """
    Решает задачу линейного программирования для максимизации минимальной маржи m.
    Возвращает словарь с ключами 'margin', 'strategy_a', 'strategy_b'.
    """
    n = len(A)
    prob = pulp.LpProblem("Maximize_Margin", pulp.LpMaximize)

    m = pulp.LpVariable("m", lowBound=0)
    x = [pulp.LpVariable(f"x_{i}", lowBound=0) for i in range(n)]
    y = [pulp.LpVariable(f"y_{j}", lowBound=0) for j in range(n)]

    prob += m
    prob += pulp.lpSum(x) == 1
    prob += pulp.lpSum(y) == 1

    for i in range(n):
        prob += pulp.lpSum(A[i][j] * y[j] for j in range(n)) >= m
    for j in range(n):
        prob += pulp.lpSum(B[i][j] * x[i] for i in range(n)) >= m

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    if prob.status != pulp.LpStatusOptimal:
        return None

    margin_opt = pulp.value(m)
    strategy_a = [pulp.value(x[i]) for i in range(n)]
    strategy_b = [pulp.value(y[j]) for j in range(n)]

    return {
        "margin": margin_opt,
        "strategy_a": strategy_a,
        "strategy_b": strategy_b
    }