from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from app.auth.oauth2 import config
from ..models.heroes import Hero
from ..services import hero_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config('GOOGLE_CLIENT_SECRET'), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


@router.get("/", name="list_heroes", response_model=List[Hero])
async def get_heroes(token: str = Depends(get_current_user)):
    return hero_service.get_all_hero()


@router.get("/{hero_id}", response_model=Hero)
async def get_hero_by_id(hero_id: int):
    return hero_service.get_by_id(hero_id)


@router.put("/{hero_id}")
async def update_hero(hero_id: int):
    hero_service.update_hero(hero_id)


@router.post("/")
async def create_hero(hero: Hero):
    hero_service.create_hero(hero)


@router.put("/")
async def bulk_update():
    hero_service.bulk_update()


@router.delete("/{hero_id}")
async def delete(hero_id: int):
    hero_service.delete(hero_id)
