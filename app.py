from fastapi import FastAPI
from login import signup_router

app = FastAPI()

app.include_router(signup_router, prefix="/signup", tags=["signup"])
