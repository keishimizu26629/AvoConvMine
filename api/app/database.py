from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_env
from urllib.parse import quote_plus

env = get_env()

if env.ENVIRONMENT == "production":
    # Heroku環境用の設定
    DATABASE_URL = env.DATABASE_URL
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # ローカル開発環境用の設定
    encoded_password = quote_plus(env.DB_PASSWORD)
    DATABASE_URL = f"postgresql://{env.DB_USER}:{encoded_password}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"

# SSLモードの設定（Heroku用）
if env.ENVIRONMENT == "production":
    Engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
else:
    Engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
BaseModel = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# デバッグ情報（オプション）
print(f"Current environment: {env.ENVIRONMENT}")
print(f"Using database URL: {'DATABASE_URL is set' if env.ENVIRONMENT == 'production' else DATABASE_URL.split('@')[1]}")
