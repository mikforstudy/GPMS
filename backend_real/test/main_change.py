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

settings = Settings()

def create_connection():
    """
    创建数据库连接，并指定使用的 schema
    """
    try:
        # 通过 options 参数设置 search_path 指定 schema
        connection = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PWD,
            options=f"-c search_path={settings.POSTGRES_SCHEMA}"
        )
        print("连接成功")
        return connection
    except OperationalError as e:
        print(f"连接失败：{e}")
        return None

def query_current_schema(connection):
    """
    查询当前连接所使用的 schema
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT current_schema();")
        current_schema = cursor.fetchone()
        print(f"当前使用的 schema: {current_schema[0]}")
    except Exception as e:
        print(f"查询出错：{e}")
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        query_current_schema(conn)
        conn.close()
