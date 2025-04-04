import os
from functools import lru_cache
from pydantic_settings import BaseSettings

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Environment(BaseSettings):
    """ 環境変数を読み込む
    """
    # データベース接続情報
    DATABASE_URL: str = None  # Heroku用
    DB_USER: str = None
    DB_PASSWORD: str = None
    DB_NAME: str = None
    DB_HOST: str = None
    DB_PORT: str = "5432"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 環境設定
    ENVIRONMENT: str = "development"

    class Config:
        env_file = os.path.join(PROJECT_ROOT, '.env')

@lru_cache
def get_env():
    """ @lru_cacheで.envの結果をキャッシュする
    """
    return Environment()
