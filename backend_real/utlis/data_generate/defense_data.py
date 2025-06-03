
import asyncio
import sys

from datetime import datetime

from app.models.project import Project
from app.models.defense import Defense
from app.models.user import User
from tortoise import Tortoise


async def generate_defense_data():
    """从projects表中获取所有项目，为每个项目创建三条答辩信息"""
    try:
        # 获取所有项目
        projects = await Project.all()

        if not projects:
            print("警告: 未找到任何项目，请确认项目表已创建且包含数据")
            return

        # 定义答辩阶段
        defense_phases = ["开题答辩", "中期答辩", "最终答辩"]

        defense_count = 0
        for project in projects:
            queryset = await User.filter(student_id=project.student_id).first()
            student_name = queryset.username if queryset else "未知学生"

            # 检查是否已有3条答辩记录
            existing_defenses = await Defense.filter(student_id=project.student_id).count()
            if existing_defenses >= 3:
                continue

            n = 1
            for phase in defense_phases:
                # 创建答辩数据
                defense_data = {
                    "project_title": project.title,
                    "student_name": student_name,
                    "student_id": project.student_id,
                    "teacher_name": project.teacher_name,
                    "defense_phase": phase,
                    "defense_class": f"教室30{n}",
                    "defense_group": f"第{n}组",
                    "status": "未开始",  # 默认状态
                    "defense_date": datetime.now().strftime("%Y-%m-%d"),
                }

                # 创建答辩记录
                await Defense.create(**defense_data)
                defense_count += 1
                n += 1

        print(f"已为{len(projects)}个项目创建了{defense_count}条答辩记录")
    except Exception as e:
        print(f"错误: {str(e)}")



# 从projects表中获取所有项目，每一条项目创建三条答辩信息，defense_phase分别为"开题答辩"、"中期答辩"、"最终答辩"

async def generate_defense_data():
    """从projects表中获取所有项目，为每个项目创建三条答辩信息"""
    # 获取所有项目
    projects = await Project.all()

    # 定义答辩阶段
    defense_phases = ["开题答辩", "中期答辩", "最终答辩"]

    defense_count = 0
    for project in projects:
        queryset = await User.filter(student_id=project.student_id).first()
        student_name = queryset.username

        # 检查是否已有3条答辩记录
        existing_defenses = await Defense.filter(student_id=project.student_id).count()
        if existing_defenses >= 3:
            continue

        n = 1
        for phase in defense_phases:
            # 创建答辩数据
            defense_data = {
                "project_title": project.title,
                "student_name": student_name,
                "student_id": project.student_id,
                "teacher_name": project.teacher_name,
                "defense_phase": phase,
                "defense_class": f"教室30{n}",
                "defense_group": f"第{n}组",
                "status": "未开始",  # 默认状态
                "defense_date": datetime.now().strftime("%Y-%m-%d"),
            }

            # 创建答辩记录
            await Defense.create(**defense_data)
            defense_count += 1
            n += 1

    print(f"已为{len(projects)}个项目创建了{defense_count}条答辩记录")


# 直接执行时的入口点
if __name__ == "__main__":
    from tortoise import Tortoise
    from app.config import TORTOISE_ORM, settings

    # 设置 Windows 兼容的事件循环策略
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # 创建配置副本并添加 schema 设置
    tortoise_config = TORTOISE_ORM.copy()
    tortoise_config["connections"]["default"]["credentials"]["schema"] = settings.POSTGRES_SCHEMA


    async def main():
        try:
            # 初始化ORM，使用包含 schema 的配置
            await Tortoise.init(config=tortoise_config)

            print(f"使用数据库架构: {settings.POSTGRES_SCHEMA}")

            # 创建数据库表
            print("正在创建数据库表...")
            await Tortoise.generate_schemas()
            print("数据库表创建完成")

            # 运行数据生成器
            await generate_defense_data()
        except Exception as e:
            print(f"错误: {str(e)}")
        finally:
            # 确保连接关闭
            await Tortoise.close_connections()

    import asyncio
    from tortoise import Tortoise
    from app.config import TORTOISE_ORM


    async def main():
        # 初始化ORM
        await Tortoise.init(config=TORTOISE_ORM)

        # 运行数据生成器
        await generate_defense_data()

        # 关闭连接
        await Tortoise.close_connections()


    # 运行异步主函数
    asyncio.run(main())