from pydantic import BaseModel

class AttributeSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
