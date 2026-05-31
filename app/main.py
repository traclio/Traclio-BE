from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.v1.endpoints.auth import router as auth_router

# 앱 구동 시 데이터베이스 테이블 및 SQLite DB 파일 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Traclio API Service",
    description="프로젝트 기록 기반 AI 포트폴리오 생성 서비스 'Traclio'의 API 백엔드입니다.",
    version="1.0.0"
)

# API 엔드포인트 포함
app.include_router(auth_router, prefix="/api/v1", tags=["사용자"])