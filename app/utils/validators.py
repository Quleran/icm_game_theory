from typing import List, Any

def validate_matrices(A: List[List[float]], B: List[List[float]]) -> None:
    """
    Проверяет корректность входных матриц.

    :raises ValueError: если матрицы не квадратные, разных размеров или содержат нечисловые значения.
    """
    if not A or not B:
        raise ValueError("Матрицы не должны быть пустыми")

    # Проверяем, что обе матрицы имеют одинаковое количество строк
    if len(A) != len(B):
        raise ValueError("Матрицы должны иметь одинаковое количество строк")

    n = len(A)

    # Проверяем, что матрицы квадратные
    for i, row in enumerate(A):
        if len(row) != n:
            raise ValueError(f"Строка {i} матрицы A имеет длину {len(row)}, ожидается {n}")
        for val in row:
            if not isinstance(val, (int, float)):
                raise ValueError(f"Элемент {val} в матрице A не является числом")

    for j, row in enumerate(B):
        if len(row) != n:
            raise ValueError(f"Строка {j} матрицы B имеет длину {len(row)}, ожидается {n}")
        for val in row:
            if not isinstance(val, (int, float)):
                raise ValueError(f"Элемент {val} в матрице B не является числом")

    # Дополнительно можно проверить, что все элементы неотрицательные (если требуется)
    # Но оставим это на усмотрение пользователя.