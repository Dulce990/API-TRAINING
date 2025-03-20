from fastapi import APIRouter, HTTPException
from typing import List
from models.image import ImageModel
from schemas.image import ImageSchema
from config.db import mongo_db

router = APIRouter()

# Obtener imágenes desde MongoDB
@router.get("/", response_model=List[ImageSchema])
async def get_images():
    try:
        images = await mongo_db["images"].find().to_list(100)  # Limita a 100 imágenes para no sobrecargar
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener imágenes: {e}")
