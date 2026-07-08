from sqlmodel import SQLModel, Field

class HeroBase(SQLModel):
    name: str = Field(min_length=2, index=True)
    age: int | None = Field(default=None, ge=0, le=150, index=True)

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str