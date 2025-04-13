from tortoise import Tortoise
from app.config import settings, TORTOISE_ORM

async def init_db():
    """初始化数据库连接，并设置 search_path"""
    await Tortoise.init(config=TORTOISE_ORM)

    # 获取默认连接并设置 search_path
    default_conn = Tortoise.get_connection("default")
    await default_conn.execute_query(f"SET search_path TO {settings.POSTGRES_SCHEMA}")

    # 生成数据库表（如果需要）
    await Tortoise.generate_schemas()

async def close_db():
    """关闭数据库连接"""
    await Tortoise.close_connections()
