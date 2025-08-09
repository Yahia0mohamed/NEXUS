# main.py
from fastapi import FastAPI
from API import code_review

app = FastAPI()
app.include_router(code_review.router)
