from pydantic import BaseModel, EmailStr


class ReaderBase(BaseModel):
    """Docstring"""
    name: str
    email: EmailStr


class ReaderCreate(ReaderBase):
    pass

class ReaderUpdate(ReaderBase):
    pass

class ReaderResponse(ReaderBase):
    id: int


    class Config:
        orm_mode = True
