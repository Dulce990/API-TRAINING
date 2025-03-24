from pydantic import BaseModel

class ImageSchema(BaseModel):
    filename: str
    contentType: str
    imageBase64: str

    class Config:
        orm_mode = True
