from fastapi import APIRouter, HTTPException
from app.models.schemas import GameRequest, GameResponse, Equilibrium
from app.services.nash_equilibrium import compute_nash_equilibrium
from app.utils.validators import validate_matrices

router = APIRouter()

@router.post("/nash", response_model=GameResponse)
async def find_nash_equilibrium(request: GameRequest):
    A = request.payoff_matrix_a
    B = request.payoff_matrix_b

    try:
        validate_matrices(A, B)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    equilibria = compute_nash_equilibrium(A, B)
    if not equilibria:
        raise HTTPException(status_code=404, detail="Равновесий не найдено")

    eq_list = [
        Equilibrium(strategy_a=list(x), strategy_b=list(y))
        for x, y in equilibria
    ]
    return GameResponse(equilibria=eq_list)