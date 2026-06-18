import pytest
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем только нужные функции без TestClient
from app.utils.validators import validate_matrices
from app.services.lp_optimizer import optimize_margin
from app.services.nash_equilibrium import compute_nash_equilibrium


# ===== 1. Тесты валидации =====
def test_valid_matrices():
    """Проверка корректных матриц"""
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    validate_matrices(A, B)  # Должно пройти без ошибок
    print("✅ test_valid_matrices passed")


def test_empty_matrices():
    """Проверка пустых матриц - должна быть ошибка"""
    with pytest.raises(ValueError):
        validate_matrices([], [])
    print("✅ test_empty_matrices passed")


def test_different_sizes():
    """Проверка матриц разных размеров"""
    A = [[1, 2], [3, 4]]
    B = [[5, 6, 7], [8, 9, 10]]
    with pytest.raises(ValueError):
        validate_matrices(A, B)
    print("✅ test_different_sizes passed")


def test_non_square():
    """Проверка неквадратной матрицы"""
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10]]
    with pytest.raises(ValueError):
        validate_matrices(A, B)
    print("✅ test_non_square passed")


def test_non_numeric():
    """Проверка нечисловых значений"""
    A = [[1, "two"], [3, 4]]
    B = [[5, 6], [7, 8]]
    with pytest.raises(ValueError):
        validate_matrices(A, B)
    print("✅ test_non_numeric passed")


# ===== 2. Тесты оптимизации LP =====
def test_basic_optimization():
    """Базовый тест оптимизации"""
    A = [[1, 2], [3, 4]]
    B = [[4, 3], [2, 1]]

    result = optimize_margin(A, B)

    assert result is not None
    assert "margin" in result
    assert "strategy_a" in result
    assert "strategy_b" in result
    assert len(result["strategy_a"]) == 2
    assert len(result["strategy_b"]) == 2
    print(f"✅ test_basic_optimization passed - margin: {result['margin']}")


def test_optimization_probabilities():
    """Проверка, что стратегии являются вероятностями"""
    A = [[1, 2], [3, 4]]
    B = [[4, 3], [2, 1]]

    result = optimize_margin(A, B)

    # Проверяем, что вероятности неотрицательные
    assert all(p >= 0 for p in result["strategy_a"])
    assert all(p >= 0 for p in result["strategy_b"])
    # Проверяем, что сумма вероятностей = 1
    assert abs(sum(result["strategy_a"]) - 1.0) < 0.001
    assert abs(sum(result["strategy_b"]) - 1.0) < 0.001
    print(f"✅ test_optimization_probabilities passed")


def test_zero_sum_game():
    """Тест игры с нулевой суммой"""
    A = [[1, -1], [-1, 1]]
    B = [[-1, 1], [1, -1]]

    result = optimize_margin(A, B)

    assert result is not None
    # В игре с нулевой суммой маржа должна быть 0
    assert abs(result["margin"]) < 0.001
    print(f"✅ test_zero_sum_game passed")


def test_3x3_optimization():
    """Тест с матрицами 3x3"""
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

    result = optimize_margin(A, B)

    assert result is not None
    assert len(result["strategy_a"]) == 3
    assert len(result["strategy_b"]) == 3
    assert abs(sum(result["strategy_a"]) - 1.0) < 0.001
    assert abs(sum(result["strategy_b"]) - 1.0) < 0.001
    print(f"✅ test_3x3_optimization passed")


def test_symmetric_game():
    """Тест симметричной игры"""
    A = [[2, 0], [0, 1]]
    B = [[2, 0], [0, 1]]

    result = optimize_margin(A, B)

    assert result is not None
    # В симметричной игре стратегии должны быть симметричны
    assert abs(result["strategy_a"][0] - result["strategy_b"][0]) < 0.001
    assert abs(result["strategy_a"][1] - result["strategy_b"][1]) < 0.001
    print(f"✅ test_symmetric_game passed")


# ===== 3. Тесты равновесий Нэша =====
def test_basic_nash():
    """Базовый тест поиска равновесий"""
    A = [[1, 2], [3, 4]]
    B = [[4, 3], [2, 1]]

    equilibria = compute_nash_equilibrium(A, B)

    assert isinstance(equilibria, list)
    assert len(equilibria) > 0
    print(f"✅ test_basic_nash passed - found {len(equilibria)} equilibria")


def test_nash_probabilities():
    """Проверка, что равновесия содержат вероятности"""
    A = [[1, 2], [3, 4]]
    B = [[4, 3], [2, 1]]

    equilibria = compute_nash_equilibrium(A, B)

    for eq in equilibria:
        strat_a, strat_b = eq
        # Проверяем, что вероятности неотрицательные
        assert all(p >= 0 for p in strat_a)
        assert all(p >= 0 for p in strat_b)
        # Проверяем, что сумма вероятностей = 1
        assert abs(sum(strat_a) - 1.0) < 0.001
        assert abs(sum(strat_b) - 1.0) < 0.001
    print(f"✅ test_nash_probabilities passed")


def test_pure_strategy_nash():
    """Тест с чистым равновесием"""
    A = [[3, 0], [0, 2]]
    B = [[1, 0], [0, 3]]

    equilibria = compute_nash_equilibrium(A, B)

    assert len(equilibria) > 0
    print(f"✅ test_pure_strategy_nash passed")


def test_mixed_strategy_nash():
    """Тест со смешанным равновесием (орлянка)"""
    A = [[1, -1], [-1, 1]]
    B = [[-1, 1], [1, -1]]

    equilibria = compute_nash_equilibrium(A, B)

    assert len(equilibria) > 0
    # В орлянке вероятности должны быть ~0.5
    for eq in equilibria:
        strat_a, strat_b = eq
        assert abs(strat_a[0] - 0.5) < 0.1
        assert abs(strat_b[0] - 0.5) < 0.1
    print(f"✅ test_mixed_strategy_nash passed")


def test_3x3_nash():
    """Тест с матрицами 3x3"""
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]

    equilibria = compute_nash_equilibrium(A, B)

    assert len(equilibria) > 0
    for eq in equilibria:
        strat_a, strat_b = eq
        assert len(strat_a) == 3
        assert len(strat_b) == 3
        assert abs(sum(strat_a) - 1.0) < 0.001
        assert abs(sum(strat_b) - 1.0) < 0.001
    print(f"✅ test_3x3_nash passed")


# ===== 4. Тесты с разными типами данных =====
def test_float_matrices():
    """Тест с числами с плавающей точкой"""
    A = [[1.5, 2.3], [3.7, 4.1]]
    B = [[4.2, 3.8], [2.6, 1.9]]

    result = optimize_margin(A, B)
    assert result is not None
    print(f"✅ test_float_matrices passed")


def test_large_values():
    """Тест с большими значениями"""
    A = [[1000, 2000], [3000, 4000]]
    B = [[4000, 3000], [2000, 1000]]

    result = optimize_margin(A, B)
    assert result is not None
    assert result["margin"] > 0
    print(f"✅ test_large_values passed")


def test_small_values():
    """Тест с маленькими значениями"""
    A = [[0.001, 0.002], [0.003, 0.004]]
    B = [[0.004, 0.003], [0.002, 0.001]]

    result = optimize_margin(A, B)
    assert result is not None
    assert result["margin"] > 0
    print(f"✅ test_small_values passed")


# ===== 5. Тесты на обработку ошибок =====
def test_validation_error_message():
    """Проверка сообщений об ошибках"""
    A = [[1, 2], [3, 4]]
    B = [[5, 6, 7]]  # Неправильный размер

    with pytest.raises(ValueError) as exc_info:
        validate_matrices(A, B)

    assert "Матрицы должны иметь одинаковое количество строк" in str(exc_info.value)
    print(f"✅ test_validation_error_message passed")


# ===== Запуск всех тестов =====
if __name__ == "__main__":
    # Запускаем все тесты
    test_valid_matrices()
    test_empty_matrices()
    test_different_sizes()
    test_non_square()
    test_non_numeric()
    test_basic_optimization()
    test_optimization_probabilities()
    test_zero_sum_game()
    test_3x3_optimization()
    test_symmetric_game()
    test_basic_nash()
    test_nash_probabilities()
    test_pure_strategy_nash()
    test_mixed_strategy_nash()
    test_3x3_nash()
    test_float_matrices()
    test_large_values()
    test_small_values()
    test_validation_error_message()

    print("\n🎉 Все тесты успешно пройдены!")