from typing import ClassVar
from os import environ
from pydantic_settings import BaseSettings
import psycopg2
from psycopg2 import OperationalError



class Settings(BaseSettings):
    """
    配置类，优先读取环境变量，不存在则使用默认值
    """
    PROJECT_NAME: str = environ.get("PROJECT_NAME", "Graduation Project Management System")
    VERSION: str = environ.get("VERSION", "0.1.0")
    DEBUG: bool = environ.get("DEBUG", True)

    # 数据库配置
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "110.41.118.235")
    POSTGRES_PORT: str = environ.get("POSTGRES_PORT", "8000")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "grad_project")
    POSTGRES_PWD: str = environ.get("POSTGRES_PWD", "Grad123@")
    POSTGRES_DB: str = environ.get("POSTGRES_DB", "mik")
    DB_POOL_MAX: int = int(environ.get("DB_POOL_MAX", 20))
    DB_POOL_CONN_LIFE: int = int(environ.get("DB_POOL_CONN_LIFE", 600))
    TIMEZONE: str = environ.get("TIMEZONE", "Asia/Shanghai")

    # 指定连接后使用的 schema
    POSTGRES_SCHEMA: str = environ.get("POSTGRES_SCHEMA", "mik_schema")

    TORTOISE_ORM: ClassVar[dict] = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.psycopg",  # 使用 psycopg 引擎

                "credentials": {
                    "database": POSTGRES_DB,
                    "host": POSTGRES_HOST,
                    "password": POSTGRES_PWD,
                    "port": POSTGRES_PORT,
                    "user": POSTGRES_USER,
                    "maxsize": DB_POOL_MAX,
                    "ssl": False,
                    "schema": POSTGRES_SCHEMA,
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

