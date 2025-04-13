import sys
import psycopg2
from psycopg2 import OperationalError
import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import sys
from contextlib import asynccontextmanager  # 新增导入

from app.config import settings, TORTOISE_ORM
from app.api.v1.endpoints import router as v1_router
from tortoise.contrib.fastapi import register_tortoise
from app.db import init_db, close_db

# 生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理数据库
    await close_db()

# 在 FastAPI 实例中注入 lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan  # 替代废弃的 on_event
)

# 注册路由
app.include_router(v1_router, prefix="/api/v1")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Windows 事件循环兼容性设置
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@app.get("/favicon.ico")
async def favicon():
    return {"message": "Favicon not found"}


@app.get("/server-status")
async def server_status():
    import platform
    import datetime
    import psutil
    from app.config import settings

    # 获取基本系统信息
    cpu_percent = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # 检查数据库连接状态
    db_status = "未连接"
    try:
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PWD,
            database=settings.POSTGRES_DB
        )
        if conn.closed == 0:
            db_status = "已连接"
        conn.close()
    except OperationalError:
        db_status = "连接失败"

    # 组装返回数据
    data = {
        "状态": "正常",
        "时间戳": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "系统信息": {
            "Python版本": sys.version,
            "FastAPI版本": fastapi.__version__,
            "操作系统": platform.system(),
            "操作系统版本": platform.version(),
            "CPU架构": platform.machine(),
            "主机名": platform.node()
        },
        "资源使用情况": {
            "CPU": {
                "使用率": f"{cpu_percent}%",
                "核心数": psutil.cpu_count()
            },
            "内存": {
                "总量": f"{round(memory.total / (1024 ** 3), 2)}GB",
                "已用": f"{round(memory.used / (1024 ** 3), 2)}GB",
                "使用率": f"{memory.percent}%"
            },
            "磁盘": {
                "总量": f"{round(disk.total / (1024 ** 3), 2)}GB",
                "已用": f"{round(disk.used / (1024 ** 3), 2)}GB",
                "使用率": f"{disk.percent}%"
            }
        },
        "数据库状态": {
            "连接状态": db_status,
            "数据库主机": settings.POSTGRES_HOST,
            "数据库名": settings.POSTGRES_DB,
            "数据库用户": settings.POSTGRES_USER
        },
        "应用配置": {
            "项目名称": settings.PROJECT_NAME,
            "版本": settings.VERSION,
            "调试模式": settings.DEBUG,
            "时区": settings.TIMEZONE
        }
    }
    return data

@app.get("/test")
def test():
    return {"message": "Hello, World!test"}
# 运行 FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)