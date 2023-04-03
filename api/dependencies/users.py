from sqlalchemy.orm import Session
from typing import List, Optional

from api.models.users import UserCreate, User
from api.auth.jwt import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password),
            is_active=True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
