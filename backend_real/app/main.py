from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.config import settings, TORTOISE_ORM
from app.api.v1.endpoints import router as v1_router



from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION, debug=settings.DEBUG)

# 注册路由
app.include_router(v1_router, prefix="/api/v1")

# 初始化Tortoise ORM
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # 开发环境下可自动生成表，生产环境请谨慎使用
    add_exception_handlers=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

