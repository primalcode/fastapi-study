from authlib.integrations.requests_client import OAuth2Session
from authlib.integrations.starlette_client import OAuth
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt
from starlette.config import Config

config = Config('.env')

oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=config('GOOGLE_CLIENT_ID'),
    client_secret=config('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)


async def authenticate_user(code: str):
    google = OAuth2Session(config('GOOGLE_CLIENT_ID'), config('GOOGLE_CLIENT_SECRET'))
    token = google.fetch_token(
        'https://accounts.google.com/o/oauth2/token',
        authorization_response=code,
        include_client_id=True,
    )
    id_info = jwt.decode(token['id_token'], options={"verify_signature": False})
    return id_info

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://accounts.google.com/o/oauth2/token",
)
