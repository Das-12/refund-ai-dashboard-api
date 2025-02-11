from fastapi import FastAPI
from app.routes import auth, logs, roles, permissions

app = FastAPI()

app.include_router(auth.router, tags=["auth"])
app.include_router(logs.router, tags=["logs"])
app.include_router(roles.router, tags=["roles"])
app.include_router(permissions.router, tags=["permissions"])