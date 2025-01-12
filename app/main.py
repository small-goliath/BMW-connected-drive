from contextlib import asynccontextmanager
import logging

from bimmer_connected.models import MyBMWAuthError
from fastapi import FastAPI, Response, Request
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask
from starlette.middleware.cors import CORSMiddleware
from starlette.types import Message
from app.bmw_account import initialize_vehicle
from app.apis.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션의 생명 주기 동안 실행할 작업 정의"""
    global vehicle
    logging.info("Starting up...")

    try:
        await initialize_vehicle()
    except MyBMWAuthError as e:
        logging.error(f"Failed to initialize vehicle: {e}")
        raise RuntimeError("Failed to initialize vehicle")

    yield

    logging.info("Shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_STR)


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}
    request._receive = receive

def log_info(req_body, res_body):
    req_body = req_body.decode('utf-8')

    logging.info(f"request body: {req_body}")
    logging.info(f"response body: {res_body}")

@app.middleware('http')
async def some_middleware(request: Request, call_next):
    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)
    
    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk
    
    task = BackgroundTask(log_info, req_body, res_body)
    return Response(content=res_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type, background=task)