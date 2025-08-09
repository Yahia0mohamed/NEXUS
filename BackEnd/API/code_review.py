from fastapi import APIRouter, HTTPException
from agents.code_review_agent import CodeReviewAgent
from models.code_review_models import CodeReviewResponse, CodeReviewRequest

router = APIRouter()
agent = CodeReviewAgent()

@router.post("/review_code", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    try:
        result = agent.review_code(request.code)  # This should return CodeReviewResponse
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")