import logging
from bimmer_connected.models import MyBMWRemoteServiceError
from fastapi import APIRouter
from app import bmw_account

router = APIRouter()

# TODO: 차량 각종 상태 조회