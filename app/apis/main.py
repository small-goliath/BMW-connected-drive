from fastapi import APIRouter

from app.apis.routes import my_car, remoting

api_router = APIRouter()
api_router.include_router(remoting.router, prefix="/remote-control", tags=["remoting"])
api_router.include_router(my_car.router, prefix="/my-car", tags=["car-data"])