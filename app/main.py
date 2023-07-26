from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.auth.oauth2 import oauth
from app.auth.oauth2 import oauth2_scheme
from .api import api_router

app = FastAPI()
app.include_router(api_router)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key")


@app.get("/auth/login/google/authorized", name="authorize")
async def authorize(request: Request):
    code = request.query_params.get("code")
    redirect_uri = str(request.url_for('authorize'))
    google = oauth.create_client('google')
    token = await google.fetch_access_token(code=code, redirect_uri=redirect_uri)

    print(f"Token: {token}")

    if not token:
        raise HTTPException(status_code=400, detail="Google OAuth code not returned")

    request.session['token'] = dict(token)

    return RedirectResponse(url=request.app.url_path_for("list_heroes"))


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('authorize')
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    return response


@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    print(f"Received token: {token}")
    return {"message": "This is a protected endpoint."}
