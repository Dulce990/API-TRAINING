from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from jose import jwt
import os
import datetime

router = APIRouter()

# Configuración de Google OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret_key")  # Llave secreta para firmar el token
JWT_ALGORITHM = "HS256"

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or not GOOGLE_REDIRECT_URI:
    raise Exception("Las variables de entorno para Google OAuth no están configuradas correctamente.")

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },
    scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
)

@router.get("/auth/google/login")
def google_login():
    try:
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        authorization_url, _ = flow.authorization_url(prompt="consent")
        return RedirectResponse(authorization_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar el flujo de autenticación: {str(e)}")

@router.get("/auth/google/callback")
def google_callback(code: str = None):
    if not code:
        raise HTTPException(status_code=400, detail="No se recibió el parámetro 'code'")
    try:
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        flow.fetch_token(code=code)
        credentials = flow.credentials
        request = Request()
        id_info = id_token.verify_oauth2_token(credentials.id_token, request, GOOGLE_CLIENT_ID)

        # Log información del usuario
        email = id_info.get("email")
        name = id_info.get("name")
        picture = id_info.get("picture")
        print(f"Usuario autenticado: email={email}, name={name}, picture={picture}")

        # Generar un token JWT con el rol de usuario
        payload = {
            "email": email,
            "name": name,
            "picture": picture,
            "role": "Usuario",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Log de redirección
        print(f"Redirigiendo a: http://localhost:8080/perfil?token={token}")
        return RedirectResponse(url=f"http://localhost:8080/perfil?token={token}")
    except Exception as e:
        print(f"Error en el callback de Google: {str(e)}")

        raise HTTPException(status_code=400, detail=f"Error al autenticar con Google: {str(e)}")
