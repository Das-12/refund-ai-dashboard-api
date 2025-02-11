from fastapi import FastAPI
from app.routes import auth, logs, roles, permissions, plans, subscriptions

app = FastAPI()

app.include_router(auth.router, tags=["auth"])
app.include_router(logs.router, tags=["logs"])
app.include_router(roles.router, tags=["roles"])
app.include_router(permissions.router, tags=["permissions"])
app.include_router(plans.router, tags=["plans"])
app.include_router(subscriptions.router, tags=["subscriptions"])