from fastapi import FastAPI
from app.routes import auth, logs

app = FastAPI()

app.include_router(auth.router)
app.include_router(logs.router)