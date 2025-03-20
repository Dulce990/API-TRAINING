from pydantic import BaseModel

class ImageModel(BaseModel):
    filename: str
    contentType: str
    imageBase64: str
