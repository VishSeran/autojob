

from fastapi import APIRouter, Request

from configs.logger import get_logger

logger = get_logger

workflow_router = APIRouter(
    prefix="/workflow",
    tags=["workflow"]
)


