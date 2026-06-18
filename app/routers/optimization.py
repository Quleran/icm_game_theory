from fastapi import APIRouter, HTTPException
from app.models.schemas import OptimizationRequest, OptimizationResponse
from app.services.lp_optimizer import optimize_margin
from app.utils.validators import validate_matrices

router = APIRouter()

@router.post("/margin", response_model=OptimizationResponse)
async def optimize_min_margin(request: OptimizationRequest):
    A = request.payoff_matrix_a
    B = request.payoff_matrix_b

    try:
        validate_matrices(A, B)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = optimize_margin(A, B)
    if result is None:
        raise HTTPException(status_code=500, detail="Не удалось решить задачу ЛП")

    return OptimizationResponse(
        optimal_margin=result["margin"],
        strategy_a=result["strategy_a"],
        strategy_b=result["strategy_b"]
    )