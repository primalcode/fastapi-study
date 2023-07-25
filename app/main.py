from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI, HTTPException, Depends
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from app.auth.oauth2 import oauth
from .api import api_router

app = FastAPI()
app.include_router(api_router)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


@app.get("/auth/login/google/authorized", name="authorize_google")
async def authorize(request: Request, token: str = Depends(oauth.google.authorize_access_token)):
    user_info = await oauth.google.parse_id_token(token)
    # ここで user_info を使用してユーザーを認証し、その情報をセッションに保存します。

    # 認証に成功したら、ユーザーを /heroes/ にリダイレクトします。
    return RedirectResponse(url=request.app.url_path_for("list_heroes"))


@app.get("/auth", name="auth")
async def read_auth(request: Request, code: str = ""):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth error: {e.error}\nDescription: {e.description}",
        )

    user = await oauth.google.parse_id_token(request, token)

    request.session["user"] = dict(user)

    return RedirectResponse(uri=request.app.url_path_for("list_heroes"))


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)
