from fastapi import APIRouter

from app.apis.routes import door

api_router = APIRouter()
api_router.include_router(door.router, prefix="/doors", tags=["doors"])