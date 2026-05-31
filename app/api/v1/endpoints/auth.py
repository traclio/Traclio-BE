from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.deps import get_current_user, security
import app.crud.auth as crud_auth
import app.schemas.auth as schemas_auth
import app.core.security as core_security
from app.models.auth import User

router = APIRouter()

# 회원가입
@router.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(user_data: schemas_auth.UserSignup, db: Session = Depends(get_db)):
    db_user = crud_auth.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    crud_auth.create_user(db=db, user=user_data)
    return {"message": "회원가입이 완료되었습니다."}

# 로그인
@router.post("/auth/login", response_model=schemas_auth.TokenResponse)
def login(credentials: schemas_auth.UserLogin, db: Session = Depends(get_db)):
    user = crud_auth.get_user_by_email(db, email=credentials.email)
    if not user or not core_security.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 잘못되었습니다."
        )
    
    access_token = core_security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# 로그아웃
@router.post("/auth/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    crud_auth.add_token_to_blacklist(db, token)
    return {"message": "성공적으로 로그아웃되었습니다."}

# 내 정보 조회
@router.get("/user/me", response_model=schemas_auth.UserMeResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# 내 정보 수정
@router.patch("/user/me", response_model=schemas_auth.UserMeResponse)
def update_me(
    update_data: schemas_auth.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = crud_auth.update_user(db, db_user=current_user, update_data=update_data)
    return updated_user