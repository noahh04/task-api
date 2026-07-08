from sqlmodel import SQLModel, Field
from models import HeroBase



class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str = Field(min_length=2)


class HeroUpdate(SQLModel):
    name: str | None = Field(default = None, min_length=2)
    age: int | None = Field(default = None, ge=0, le=150)
    secret_name: str | None = Field(default = None, min_length=2)
