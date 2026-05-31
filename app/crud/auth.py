from sqlalchemy.orm import Session
from app.models.auth import User, BlacklistedToken
from app.schemas.auth import UserSignup, UserUpdate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserSignup):
    hashed_pw = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_pw,
        nickname=user.nickname
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, update_data: UserUpdate):
    if update_data.nickname is not None:
        db_user.nickname = update_data.nickname
    if update_data.profile_image is not None:
        db_user.profile_image = update_data.profile_image
    db.commit()
    db.refresh(db_user)
    return db_user

def add_token_to_blacklist(db: Session, token: str):
    db_token = BlacklistedToken(token=token)
    db.add(db_token)
    db.commit()

def is_token_blacklisted(db: Session, token: str) -> bool:
    return db.query(BlacklistedToken).filter(BlacklistedToken.token == token).first() is not None