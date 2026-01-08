from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    index: Optional[int] = None
    name_fa: Optional[str] = None
    name_en: Optional[str] = None
    website: Optional[str] = None
    website_desc: Optional[str] = None
    magazine_desc: Optional[str] = None
    file_number: Optional[int] = None
    sector: Optional[str] = None
    country: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str