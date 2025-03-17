from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "defenses" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "project_title" VARCHAR(100) NOT NULL,
    "defense_class" VARCHAR(50) NOT NULL,
    "defense_group" VARCHAR(50) NOT NULL,
    "defense_phase" VARCHAR(50) NOT NULL,
    "defense_date" DATE NOT NULL,
    "student_name" VARCHAR(50) NOT NULL,
    "student_id" INT NOT NULL,
    "teacher_name" VARCHAR(50) NOT NULL,
    "created_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(20) NOT NULL DEFAULT '未开始'
);
COMMENT ON COLUMN "defenses"."id" IS '主键';
COMMENT ON COLUMN "defenses"."project_title" IS '项目标题';
COMMENT ON COLUMN "defenses"."defense_class" IS '答辩教室';
COMMENT ON COLUMN "defenses"."defense_group" IS '答辩组';
COMMENT ON COLUMN "defenses"."defense_phase" IS '答辩阶段';
COMMENT ON COLUMN "defenses"."defense_date" IS '答辩日期';
COMMENT ON COLUMN "defenses"."student_name" IS '学生姓名';
COMMENT ON COLUMN "defenses"."student_id" IS '学生ID';
COMMENT ON COLUMN "defenses"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "defenses"."status" IS '状态';
COMMENT ON TABLE "defenses" IS '答辩表，用于记录答辩信息。';
CREATE TABLE IF NOT EXISTS "middle_docxs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "mark" VARCHAR(50) NOT NULL DEFAULT '中期检查',
    "title" VARCHAR(100) NOT NULL,
    "student_name" VARCHAR(50) NOT NULL,
    "student_id" INT NOT NULL,
    "teacher_name" VARCHAR(50) NOT NULL,
    "content1" TEXT NOT NULL,
    "content6" TEXT NOT NULL,
    "content7" TEXT NOT NULL,
    "created_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(20) NOT NULL DEFAULT '待审核'
);
COMMENT ON COLUMN "middle_docxs"."id" IS '主键';
COMMENT ON COLUMN "middle_docxs"."mark" IS '标记';
COMMENT ON COLUMN "middle_docxs"."title" IS '中期检查标题';
COMMENT ON COLUMN "middle_docxs"."student_name" IS '学生姓名';
COMMENT ON COLUMN "middle_docxs"."student_id" IS '学生ID';
COMMENT ON COLUMN "middle_docxs"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "middle_docxs"."content1" IS '第一部分内容';
COMMENT ON COLUMN "middle_docxs"."content6" IS '第六部分内容';
COMMENT ON COLUMN "middle_docxs"."content7" IS '第七部分内容';
COMMENT ON COLUMN "middle_docxs"."status" IS '状态';
COMMENT ON TABLE "middle_docxs" IS '中期检查表，用于记录中期检查信息。';
CREATE TABLE IF NOT EXISTS "projects" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(100) NOT NULL,
    "description" TEXT,
    "status" VARCHAR(20) NOT NULL,
    "start_date" DATE NOT NULL,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "end_date" DATE,
    "teacher_id" INT NOT NULL,
    "student_id" INT NOT NULL,
    "teacher_name" VARCHAR(50) NOT NULL
);
COMMENT ON COLUMN "projects"."id" IS '主键ID';
COMMENT ON COLUMN "projects"."title" IS '项目标题';
COMMENT ON COLUMN "projects"."description" IS '项目描述';
COMMENT ON COLUMN "projects"."status" IS '项目状态（开题，中期，项目答辩，完成）';
COMMENT ON COLUMN "projects"."start_date" IS '开始日期';
COMMENT ON COLUMN "projects"."update_time" IS '更新日期';
COMMENT ON COLUMN "projects"."end_date" IS '结束日期';
COMMENT ON COLUMN "projects"."teacher_id" IS '导师ID';
COMMENT ON COLUMN "projects"."student_id" IS '学生ID';
COMMENT ON COLUMN "projects"."teacher_name" IS '导师姓名';
COMMENT ON TABLE "projects" IS '项目表，用于记录项目信息。';
CREATE TABLE IF NOT EXISTS "scores" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "project_title" VARCHAR(100) NOT NULL,
    "student_name" VARCHAR(50) NOT NULL,
    "student_id" INT NOT NULL,
    "teacher_name" VARCHAR(50) NOT NULL,
    "score" VARCHAR(50) NOT NULL,
    "created_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "scores"."id" IS '主键';
COMMENT ON COLUMN "scores"."project_title" IS '项目标题';
COMMENT ON COLUMN "scores"."student_name" IS '学生姓名';
COMMENT ON COLUMN "scores"."student_id" IS '学生ID';
COMMENT ON COLUMN "scores"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "scores"."score" IS '成绩';
COMMENT ON TABLE "scores" IS '成绩表，用于记录成绩信息。';
CREATE TABLE IF NOT EXISTS "selections" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "major" VARCHAR(100) NOT NULL,
    "student_id" INT NOT NULL,
    "teacher_id" INT NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "status" VARCHAR(50) NOT NULL DEFAULT '待审核',
    "created_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "selections"."id" IS '主键';
COMMENT ON COLUMN "selections"."username" IS '用户名';
COMMENT ON COLUMN "selections"."major" IS '专业';
COMMENT ON TABLE "selections" IS '选题表，用于记录选题信息。';
CREATE TABLE IF NOT EXISTS "start_docxs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "mark" VARCHAR(50) NOT NULL DEFAULT '开题报告',
    "title" VARCHAR(100) NOT NULL,
    "student_name" VARCHAR(50) NOT NULL,
    "student_id" INT NOT NULL,
    "teacher_name" VARCHAR(50) NOT NULL,
    "content1" TEXT NOT NULL,
    "content2" TEXT NOT NULL,
    "content3" TEXT NOT NULL,
    "content4" TEXT NOT NULL,
    "content5" TEXT NOT NULL,
    "content6" TEXT NOT NULL,
    "created_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(20) NOT NULL DEFAULT '待审核'
);
COMMENT ON COLUMN "start_docxs"."id" IS '主键';
COMMENT ON COLUMN "start_docxs"."mark" IS '标记';
COMMENT ON COLUMN "start_docxs"."title" IS '开题报告标题';
COMMENT ON COLUMN "start_docxs"."student_name" IS '学生姓名';
COMMENT ON COLUMN "start_docxs"."student_id" IS '学生ID';
COMMENT ON COLUMN "start_docxs"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "start_docxs"."content1" IS '第一部分内容';
COMMENT ON COLUMN "start_docxs"."content2" IS '第二部分内容';
COMMENT ON COLUMN "start_docxs"."content3" IS '第三部分内容';
COMMENT ON COLUMN "start_docxs"."content4" IS '第四部分内容';
COMMENT ON COLUMN "start_docxs"."content5" IS '第五部分内容';
COMMENT ON COLUMN "start_docxs"."content6" IS '第六部分内容';
COMMENT ON COLUMN "start_docxs"."status" IS '状态';
COMMENT ON TABLE "start_docxs" IS '开题报告表，用于记录开题报告信息。';
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "role" VARCHAR(100) NOT NULL,
    "student_id" INT NOT NULL,
    "teacher_id" INT NOT NULL,
    "created_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."id" IS '主键';
COMMENT ON TABLE "users" IS '用户表，用于记录用户信息。';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
