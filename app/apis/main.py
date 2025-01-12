from fastapi import APIRouter

from app.apis.routes import remoting

api_router = APIRouter()
api_router.include_router(remoting.router, prefix="/remote-control", tags=["remoting"])