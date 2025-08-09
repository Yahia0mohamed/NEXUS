from pydantic import BaseModel

class CodeReviewRequest(BaseModel):
    code: str

class CodeReviewResponse(BaseModel):
    improved_code: str
    explanation: str