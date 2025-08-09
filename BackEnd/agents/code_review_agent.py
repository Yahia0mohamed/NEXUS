from services.gemini_client import GeminiClient
from services.vector_DB import VectorDB
import json
from models.code_review_models import CodeReviewResponse

class CodeReviewAgent:
    def __init__(self):
        self.gemini = GeminiClient()
        self.vector_db = VectorDB()
    
    def review_code(self, code: str) -> str:

        self.vector_db.add_document(code, metadata={"type": "user_submission"})
        # Retrieve relevant context from Vector DB (optional)
        context = self.vector_db.retrieve_similar(code, top_k=5)

        # Build structured prompt
        prompt = f"""
        You are a senior software engineer.
        Review and improve the following code based on:
        - Clean Code principles
        - SOLID principles
        - DRY concept
        - Efficiency
        - Relevant design patterns

        Return your answer strictly as JSON in this format:
        {{
          "improved_code": "string",
          "explanation": "string"
        }}

        Context from existing codebase:
        {context}

        CODE:
        ```
        {code}
        ```
        """

        # Call Gemini
        raw_output = self.gemini.generate_content(prompt)

        try:
            parsed = json.loads(raw_output)
            return CodeReviewResponse(**parsed)
        except json.JSONDecodeError:
            raise ValueError(f"Gemini did not return valid JSON: {raw_output}")