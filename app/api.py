from fastapi import APIRouter

from app.endpoints import hero

api_router = APIRouter()
api_router.include_router(hero.router, prefix="/heroes", tags=["heroes"])
