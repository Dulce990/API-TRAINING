from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import mongo_db
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from routes.usuarios import router as usuario_router
from routes.expediente_medicoRoutes import router as expediente_medico_router
from routes.dietas import router as dietas_router
from routes.ejercicios import router as ejercicios_router  
from routes.indicadores_nutricionales import router as indicadores_nutricionales_router
from routes.objetivo_programa import router as objetivo_programa_router
from routes.rutinas import router as rutinas_router
from routes.programas_saludables import router as programas_saludables_router
from routes.images import router as image_router
from utils.socket_manager import init_socket_manager  # Importa la función de inicialización
from routes.google_auth import router as google_auth_router
from dotenv import load_dotenv
from routes.usuarios_rol import router as usuarios_rol_router
from routes.health import router as health_router
load_dotenv()

# Creación de la aplicación FastAPI
app = FastAPI(
    title="Gimnasio API",
    description="API para gestionar usuarios, expedientes médicos, dietas y ejercicios del gimnasio"
)

# Permitir solicitudes desde el frontend (localhost:8080)
origins = [
    "http://localhost:8080",  # Tu app de Vue
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # Puedes restringirlo a dominios específicos si lo deseas
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Inicializar Socket.IO
init_socket_manager(app)

# Incluir las rutas de los módulos
app.include_router(ejercicios_router, prefix="/api", tags=["Ejercicios"])
app.include_router(usuario_router, prefix="/api", tags=["Usuarios"])
app.include_router(expediente_medico_router, prefix="/api", tags=["Expediente Médico"])
app.include_router(dietas_router, prefix="/api", tags=["Dietas"])
app.include_router(ejercicios_router, prefix="/api", tags=["Ejercicios"])  
app.include_router(indicadores_nutricionales_router, prefix="/api", tags=["Indicadores Nutricionales"])
app.include_router(objetivo_programa_router, prefix="/api", tags=["Objetivos del Programa"])
app.include_router(programas_saludables_router, prefix="/api", tags=["Programas Saludables"])
app.include_router(rutinas_router, prefix="/api", tags=["Rutinas"])
app.include_router(image_router, prefix="/api/images", tags=["Images"])
app.include_router(google_auth_router, prefix="/api", tags=["Google Auth"])
app.include_router(usuarios_rol_router, prefix="/api", tags=["Usuarios Rol"])
app.include_router(health_router, prefix="/api", tags=["Health"])

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:  # Error de autenticación
        return JSONResponse(
            status_code=404,  # Cambiar el código de estado a 404
            content={"detail": "Ruta no encontrada"},
        )
    elif exc.status_code == 404:  # Ruta no encontrada
        return JSONResponse(
            status_code=404,
            content={"detail": "Ruta no encontrada"},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

