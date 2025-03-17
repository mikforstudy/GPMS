from os import environ
from typing import ClassVar
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    配置类，优先读取环境变量，不存在则使用默认值
    """
    PROJECT_NAME: str = environ.get("PROJECT_NAME", "Graduation Project Management System")
    VERSION: str = environ.get("VERSION", "0.1.0")
    DEBUG: bool = environ.get("DEBUG", True)

    # 数据库配置
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_PORT: str = environ.get("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PWD: str = environ.get("POSTGRES_PWD", "admin")
    POSTGRES_DB: str = environ.get("POSTGRES_DB", "postgres_demo")
    DB_POOL_MAX: int = int(environ.get("DB_POOL_MAX", 20))
    DB_POOL_CONN_LIFE: int = int(environ.get("DB_POOL_CONN_LIFE", 600))
    TIMEZONE: str = environ.get("TIMEZONE", "Asia/Shanghai")

    TORTOISE_ORM: ClassVar[dict] = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "database": POSTGRES_DB,
                    "host": POSTGRES_HOST,
                    "password": POSTGRES_PWD,
                    "port": POSTGRES_PORT,
                    "user": POSTGRES_USER,
                    "maxsize": DB_POOL_MAX,
                    "ssl": False
                },
            }
        },
        "apps": {
            "models": {
                "models": ["aerich.models", "app.models"],
                "default_connection": "default",
            }
        },
        "use_tz": False,
        "timezone": TIMEZONE
    }

settings = Settings()
TORTOISE_ORM = settings.TORTOISE_ORM



