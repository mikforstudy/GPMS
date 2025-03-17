from datetime import datetime

from app.models.project import Project
from app.models.defense import Defense
from app.models.user import User


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