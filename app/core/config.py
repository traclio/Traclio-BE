import os

SECRET_KEY = os.getenv("SECRET_KEY", "traclio-sprint-temporary-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
DATABASE_URL = "sqlite:///./traclio.db"  # 프로젝트명 'Traclio'에 맞게 수정됨