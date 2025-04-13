from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "end_docxs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "mark" VARCHAR(50) NOT NULL DEFAULT '最终答辩',
    "title" VARCHAR(100) NOT NULL,
    "student_name" VARCHAR(50) NOT NULL,
    "student_id" INT NOT NULL,
    "teacher_name" VARCHAR(50) NOT NULL,
    "content1" TEXT NOT NULL,
    "content2" TEXT NOT NULL,
    "content3" TEXT NOT NULL,
    "content4" TEXT NOT NULL,
    "created_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(20) NOT NULL DEFAULT '待审核'
);
COMMENT ON COLUMN "end_docxs"."id" IS '主键';
COMMENT ON COLUMN "end_docxs"."mark" IS '标记';
COMMENT ON COLUMN "end_docxs"."title" IS '毕业设计题目';
COMMENT ON COLUMN "end_docxs"."student_name" IS '学生姓名';
COMMENT ON COLUMN "end_docxs"."student_id" IS '学生ID';
COMMENT ON COLUMN "end_docxs"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "end_docxs"."content1" IS '第一部分内容';
COMMENT ON COLUMN "end_docxs"."content2" IS '第二部分内容';
COMMENT ON COLUMN "end_docxs"."content3" IS '第三部分内容';
COMMENT ON COLUMN "end_docxs"."content4" IS '第四部分内容';
COMMENT ON COLUMN "end_docxs"."status" IS '状态';
COMMENT ON TABLE "end_docxs" IS '最终答辩表，用于记录最终答辩信息。';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "end_docxs";"""
