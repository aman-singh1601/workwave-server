from fastapi import FastAPI
from auth.signup import signup_router
from auth.login import login_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
"*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(signup_router, prefix="/api")
app.include_router(login_router, prefix="/api")