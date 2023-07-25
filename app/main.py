from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth.oauth2 import oauth
from .api import api_router

app = FastAPI()
app.include_router(api_router)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


@app.get("/auth/login/google/authorized", name="authorize")
async def authorize(request: Request):
    print("###### START authorize")

    print(request.query_params)

    # authorize時のセッション値を出力
    print(f"Session at authorize: {request.session.items()}")

    token = request.query_params.get("code")
    if not token:
        raise HTTPException(status_code=400, detail="Google OAuth code not returned")

    # 正確にはこれはアクセストークンである
    token = await oauth.google.authorize_access_token(request)

    if not token:
        raise HTTPException(status_code=400, detail="Invalid token")

    # Add the access token to the session for later use
    request.session['token'] = dict(token)

    # Use the token to get user info
    user_info = await oauth.google.userinfo(token=token)

    print(f"User info: {user_info}")  # この行を追加

    # 認証に成功したら、ユーザーを /heroes/ にリダイレクトします。
    return RedirectResponse(url=request.app.url_path_for("list_heroes"))


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('authorize')
    response = await oauth.google.authorize_redirect(request, redirect_uri)

    # 追加: ログイン時のセッション値を出力
    print(f"Session after login: {request.session.items()}")

    return response
