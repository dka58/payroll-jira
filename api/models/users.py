from sqlalchemy import Column, Integer, String
from api.utils.database import Base
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    def __repr__(self):
        return f"<User {self.username}>"
    

class UserInDBBase(BaseModel):
    email: str
    username: str
    class Config:
        orm_mode = True


class UserCreate(UserInDBBase):
    password: str


class UserUpdate(UserInDBBase):
    password: str


class UserInDB(UserInDBBase):
    hashed_password: str