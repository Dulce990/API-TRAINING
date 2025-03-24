from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import mongo_db
# Importación de los routers
from routes.usuarios import router as usuario_router
from routes.expediente_medicoRoutes import router as expediente_medico_router
from routes.dietas import router as dietas_router
from routes.ejercicios import router as ejercicios_router  
from routes.indicadores_nutricionales import router as indicadores_nutricionales_router
from routes.objetivo_programa import router as objetivo_programa_router
from routes.rutinas import router as rutinas_router
from routes.programas_saludables import router as programas_saludables_router
from routes.auth import auth_router
from routes.images import router as image_router

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

# Incluir las rutas de los módulos
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])  # Agregar las rutas de autenticación
app.include_router(usuario_router, prefix="/api", tags=["Usuarios"])
app.include_router(expediente_medico_router, prefix="/api", tags=["Expediente Médico"])
app.include_router(dietas_router, prefix="/api", tags=["Dietas"])
app.include_router(ejercicios_router, prefix="/api", tags=["Ejercicios"])  
app.include_router(indicadores_nutricionales_router, prefix="/api", tags=["Indicadores Nutricionales"])
app.include_router(objetivo_programa_router, prefix="/api", tags=["Objetivos del Programa"])
app.include_router(programas_saludables_router, prefix="/api", tags=["Programas Saludables"])
app.include_router(rutinas_router, prefix="/api", tags=["Rutinas"])
app.include_router(auth_router, prefix="/api", tags=["Auth"])
app.include_router(image_router, prefix="/api/images", tags=["Images"])



