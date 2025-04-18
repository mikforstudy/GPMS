/*
 Navicat Premium Dump SQL

 Source Server         : grad_project
 Source Server Type    : GaussDB
 Source Server Version : 90204 (GaussDB 8.2)
 Source Host           : 110.41.118.235:8000
 Source Catalog        : mik
 Source Schema         : mik_schema

 Target Server Type    : GaussDB
 Target Server Version : 90204 (GaussDB 8.2)
 File Encoding         : 65001

 Date: 18/04/2025 11:19:39
*/


-- ----------------------------
-- Sequence structure for aerich_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."aerich_id_seq";
CREATE SEQUENCE "mik_schema"."aerich_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for defenses_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."defenses_id_seq";
CREATE SEQUENCE "mik_schema"."defenses_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for end_docxs_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."end_docxs_id_seq";
CREATE SEQUENCE "mik_schema"."end_docxs_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for groups_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."groups_id_seq";
CREATE SEQUENCE "mik_schema"."groups_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for middle_docxs_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."middle_docxs_id_seq";
CREATE SEQUENCE "mik_schema"."middle_docxs_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for phase_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."phase_id_seq";
CREATE SEQUENCE "mik_schema"."phase_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for projects_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."projects_id_seq";
CREATE SEQUENCE "mik_schema"."projects_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for score_docx_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."score_docx_id_seq";
CREATE SEQUENCE "mik_schema"."score_docx_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for scores_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."scores_id_seq";
CREATE SEQUENCE "mik_schema"."scores_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for selections_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."selections_id_seq";
CREATE SEQUENCE "mik_schema"."selections_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for start_docxs_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."start_docxs_id_seq";
CREATE SEQUENCE "mik_schema"."start_docxs_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "mik_schema"."users_id_seq";
CREATE SEQUENCE "mik_schema"."users_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for aerich
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."aerich";
CREATE TABLE "mik_schema"."aerich" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".aerich_id_seq'::regclass),
  "version" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "app" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "content" jsonb NOT NULL
)
WITH (orientation=ROW, storage_type=USTORE)
;

-- ----------------------------
-- Records of aerich
-- ----------------------------

-- ----------------------------
-- Table structure for defenses
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."defenses";
CREATE TABLE "mik_schema"."defenses" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".defenses_id_seq'::regclass),
  "project_title" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "defense_class" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "defense_group" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "defense_phase" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "defense_date" date NOT NULL,
  "student_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "student_id" int4 NOT NULL,
  "teacher_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "created_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "update_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "status" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '未开始'::character varying
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."defenses"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."defenses"."project_title" IS '项目标题';
COMMENT ON COLUMN "mik_schema"."defenses"."defense_class" IS '答辩教室';
COMMENT ON COLUMN "mik_schema"."defenses"."defense_group" IS '答辩组';
COMMENT ON COLUMN "mik_schema"."defenses"."defense_phase" IS '答辩阶段';
COMMENT ON COLUMN "mik_schema"."defenses"."defense_date" IS '答辩日期';
COMMENT ON COLUMN "mik_schema"."defenses"."student_name" IS '学生姓名';
COMMENT ON COLUMN "mik_schema"."defenses"."student_id" IS '学生ID';
COMMENT ON COLUMN "mik_schema"."defenses"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "mik_schema"."defenses"."status" IS '状态';
COMMENT ON TABLE "mik_schema"."defenses" IS '答辩表，用于记录答辩信息。';

-- ----------------------------
-- Records of defenses
-- ----------------------------
INSERT INTO "mik_schema"."defenses" VALUES (1, '测试题目1', '教室301', '第1组', '开题答辩', '2025-03-30', 'student1', 1, 'teacher1', '2025-03-30 17:25:39.587537+08', '2025-04-04 22:12:12.096954+08', '已完成');
INSERT INTO "mik_schema"."defenses" VALUES (2, '测试题目1', '教室302', '第2组', '中期答辩', '2025-03-30', 'student1', 1, 'teacher1', '2025-03-30 17:25:39.632371+08', '2025-03-30 17:25:39.632371+08', '未开始');
INSERT INTO "mik_schema"."defenses" VALUES (3, '测试题目1', '教室303', '第3组', '最终答辩', '2025-03-30', 'student1', 1, 'teacher1', '2025-03-30 17:25:39.674844+08', '2025-03-30 17:25:39.674844+08', '未开始');
INSERT INTO "mik_schema"."defenses" VALUES (4, '测试题目2', '教室301', '第1组', '开题答辩', '2025-03-30', 'student2', 2, 'teacher1', '2025-03-30 17:25:39.796751+08', '2025-03-30 17:25:39.796751+08', '未开始');
INSERT INTO "mik_schema"."defenses" VALUES (5, '测试题目2', '教室302', '第2组', '中期答辩', '2025-03-30', 'student2', 2, 'teacher1', '2025-03-30 17:25:39.841826+08', '2025-03-30 17:25:39.841826+08', '未开始');
INSERT INTO "mik_schema"."defenses" VALUES (6, '测试题目2', '教室303', '第3组', '最终答辩', '2025-03-30', 'student2', 2, 'teacher1', '2025-03-30 17:25:39.885644+08', '2025-03-30 17:25:39.885644+08', '未开始');
INSERT INTO "mik_schema"."defenses" VALUES (7, '测试题目3', '教室301', '第1组', '开题答辩', '2025-03-30', 'student3', 3, 'teacher1', '2025-03-30 17:25:40.048739+08', '2025-03-30 17:25:40.048739+08', '未开始');
INSERT INTO "mik_schema"."defenses" VALUES (8, '测试题目3', '教室302', '第2组', '中期答辩', '2025-03-30', 'student3', 3, 'teacher1', '2025-03-30 17:25:40.090638+08', '2025-03-30 17:25:40.090638+08', '未开始');
INSERT INTO "mik_schema"."defenses" VALUES (9, '测试题目3', '教室303', '第3组', '最终答辩', '2025-03-30', 'student3', 3, 'teacher1', '2025-03-30 17:25:40.134858+08', '2025-03-30 17:25:40.134858+08', '未开始');

-- ----------------------------
-- Table structure for end_docxs
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."end_docxs";
CREATE TABLE "mik_schema"."end_docxs" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".end_docxs_id_seq'::regclass),
  "mark" varchar(50) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '最终答辩'::character varying,
  "title" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "student_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "student_id" int4 NOT NULL,
  "teacher_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "content1" text COLLATE "pg_catalog"."default" NOT NULL,
  "content2" text COLLATE "pg_catalog"."default" NOT NULL,
  "content3" text COLLATE "pg_catalog"."default" NOT NULL,
  "content4" text COLLATE "pg_catalog"."default" NOT NULL,
  "created_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "update_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "status" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '待审核'::character varying
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."end_docxs"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."end_docxs"."mark" IS '标记';
COMMENT ON COLUMN "mik_schema"."end_docxs"."title" IS '毕业设计题目';
COMMENT ON COLUMN "mik_schema"."end_docxs"."student_name" IS '学生姓名';
COMMENT ON COLUMN "mik_schema"."end_docxs"."student_id" IS '学生ID';
COMMENT ON COLUMN "mik_schema"."end_docxs"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "mik_schema"."end_docxs"."content1" IS '第一部分内容';
COMMENT ON COLUMN "mik_schema"."end_docxs"."content2" IS '第二部分内容';
COMMENT ON COLUMN "mik_schema"."end_docxs"."content3" IS '第三部分内容';
COMMENT ON COLUMN "mik_schema"."end_docxs"."content4" IS '第四部分内容';
COMMENT ON COLUMN "mik_schema"."end_docxs"."status" IS '状态';
COMMENT ON TABLE "mik_schema"."end_docxs" IS '最终答辩表，用于记录最终答辩信息。';

-- ----------------------------
-- Records of end_docxs
-- ----------------------------
INSERT INTO "mik_schema"."end_docxs" VALUES (1, '最终答辩', '测试题目3', 'student3', 3, 'teacher1', '待填写111', '待填写111', '待填写11', '待填写11', '2025-03-30 12:01:02.232192+08', '2025-03-30 12:01:02.232192+08', '待审核');

-- ----------------------------
-- Table structure for groups
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."groups";
CREATE TABLE "mik_schema"."groups" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".groups_id_seq'::regclass),
  "student_id" int4 NOT NULL,
  "student_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "teacher_name1" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "teacher_name2" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "teacher_name3" varchar(50) COLLATE "pg_catalog"."default" NOT NULL
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."groups"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."groups"."student_id" IS '学生ID';
COMMENT ON COLUMN "mik_schema"."groups"."student_name" IS '学生姓名';
COMMENT ON COLUMN "mik_schema"."groups"."teacher_name1" IS '受邀评阅教师1';
COMMENT ON COLUMN "mik_schema"."groups"."teacher_name2" IS '受邀评阅教师2';
COMMENT ON COLUMN "mik_schema"."groups"."teacher_name3" IS '受邀评阅教师3';

-- ----------------------------
-- Records of groups
-- ----------------------------
INSERT INTO "mik_schema"."groups" VALUES (1, 1, 'student1', 'teacher1', 'teacher2', 'teacher3');
INSERT INTO "mik_schema"."groups" VALUES (2, 2, 'student2', 'teacher2', 'teacher3', 'teacher1');
INSERT INTO "mik_schema"."groups" VALUES (3, 3, 'student3', 'teacher3', 'teacher1', 'teacher2');
INSERT INTO "mik_schema"."groups" VALUES (4, 4, '4', '4', '4', '4');

-- ----------------------------
-- Table structure for middle_docxs
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."middle_docxs";
CREATE TABLE "mik_schema"."middle_docxs" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".middle_docxs_id_seq'::regclass),
  "mark" varchar(50) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '中期检查'::character varying,
  "title" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "student_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "student_id" int4 NOT NULL,
  "teacher_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "content1" text COLLATE "pg_catalog"."default" NOT NULL,
  "content6" text COLLATE "pg_catalog"."default" NOT NULL,
  "content7" text COLLATE "pg_catalog"."default" NOT NULL,
  "created_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "update_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "status" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '待审核'::character varying
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."middle_docxs"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."mark" IS '标记';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."title" IS '中期检查标题';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."student_name" IS '学生姓名';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."student_id" IS '学生ID';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."content1" IS '第一部分内容';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."content6" IS '第六部分内容';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."content7" IS '第七部分内容';
COMMENT ON COLUMN "mik_schema"."middle_docxs"."status" IS '状态';
COMMENT ON TABLE "mik_schema"."middle_docxs" IS '中期检查表，用于记录中期检查信息。';

-- ----------------------------
-- Records of middle_docxs
-- ----------------------------

-- ----------------------------
-- Table structure for phase
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."phase";
CREATE TABLE "mik_schema"."phase" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".phase_id_seq'::regclass),
  "time1_1" date NOT NULL,
  "time1_2" date NOT NULL,
  "time2_1" date NOT NULL,
  "time2_2" date NOT NULL,
  "time3_1" date NOT NULL,
  "time3_2" date NOT NULL,
  "time4_1" date NOT NULL,
  "time4_2" date NOT NULL,
  "time5_1" date NOT NULL,
  "time5_2" date NOT NULL
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."phase"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."phase"."time1_1" IS '选题开始时间';
COMMENT ON COLUMN "mik_schema"."phase"."time1_2" IS '选题结束时间';
COMMENT ON COLUMN "mik_schema"."phase"."time2_1" IS '开题开始时间';
COMMENT ON COLUMN "mik_schema"."phase"."time2_2" IS '开题结束时间';
COMMENT ON COLUMN "mik_schema"."phase"."time3_1" IS '中期开始时间';
COMMENT ON COLUMN "mik_schema"."phase"."time3_2" IS '中期结束时间';
COMMENT ON COLUMN "mik_schema"."phase"."time4_1" IS '论文开始时间';
COMMENT ON COLUMN "mik_schema"."phase"."time4_2" IS '论文结束时间';
COMMENT ON COLUMN "mik_schema"."phase"."time5_1" IS '答辩开始时间';
COMMENT ON COLUMN "mik_schema"."phase"."time5_2" IS '答辩结束时间';

-- ----------------------------
-- Records of phase
-- ----------------------------
INSERT INTO "mik_schema"."phase" VALUES (1, '2024-12-29', '2025-01-29', '2025-01-30', '2025-02-27', '2025-02-28', '2025-03-30', '2025-03-31', '2025-04-29', '2025-04-30', '2025-05-16');

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."projects";
CREATE TABLE "mik_schema"."projects" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".projects_id_seq'::regclass),
  "title" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "status" varchar(20) COLLATE "pg_catalog"."default" NOT NULL,
  "start_date" date NOT NULL,
  "update_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "end_date" date,
  "teacher_id" int4 NOT NULL,
  "student_id" int4 NOT NULL,
  "teacher_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."projects"."id" IS '主键ID';
COMMENT ON COLUMN "mik_schema"."projects"."title" IS '项目标题';
COMMENT ON COLUMN "mik_schema"."projects"."description" IS '项目描述';
COMMENT ON COLUMN "mik_schema"."projects"."status" IS '项目状态（开题，中期，项目答辩，完成）';
COMMENT ON COLUMN "mik_schema"."projects"."start_date" IS '开始日期';
COMMENT ON COLUMN "mik_schema"."projects"."update_time" IS '更新日期';
COMMENT ON COLUMN "mik_schema"."projects"."end_date" IS '结束日期';
COMMENT ON COLUMN "mik_schema"."projects"."teacher_id" IS '导师ID';
COMMENT ON COLUMN "mik_schema"."projects"."student_id" IS '学生ID';
COMMENT ON COLUMN "mik_schema"."projects"."teacher_name" IS '导师姓名';
COMMENT ON TABLE "mik_schema"."projects" IS '项目表，用于记录项目信息。';

-- ----------------------------
-- Records of projects
-- ----------------------------
INSERT INTO "mik_schema"."projects" VALUES (1, '测试题目1', '测试题目1描述', '开题', '2025-03-28', '2025-03-28 21:03:10.908519+08', NULL, 1, 1, 'teacher1');
INSERT INTO "mik_schema"."projects" VALUES (2, '测试题目2', '测试题目描述2', '开题', '2025-03-30', '2025-03-30 02:12:09.280547+08', NULL, 1, 2, 'teacher1');
INSERT INTO "mik_schema"."projects" VALUES (3, '测试题目3', '测试题目3描述', '通过开题报告', '2025-03-30', '2025-03-30 12:03:56.754424+08', NULL, 1, 3, 'teacher1');

-- ----------------------------
-- Table structure for score_docx
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."score_docx";
CREATE TABLE "mik_schema"."score_docx" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".score_docx_id_seq'::regclass),
  "student_id" int4,
  "student_name" varchar(50) COLLATE "pg_catalog"."default",
  "content1" varchar(50) COLLATE "pg_catalog"."default",
  "score1" int4,
  "content2" varchar(50) COLLATE "pg_catalog"."default",
  "score2" int4,
  "content3" varchar(50) COLLATE "pg_catalog"."default",
  "score3" int4,
  "score4" int4
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."score_docx"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."score_docx"."student_id" IS '学生ID';
COMMENT ON COLUMN "mik_schema"."score_docx"."student_name" IS '学生姓名';
COMMENT ON COLUMN "mik_schema"."score_docx"."content1" IS '评语1';
COMMENT ON COLUMN "mik_schema"."score_docx"."score1" IS '评语1分数';
COMMENT ON COLUMN "mik_schema"."score_docx"."content2" IS '评语2';
COMMENT ON COLUMN "mik_schema"."score_docx"."score2" IS '评语2分数';
COMMENT ON COLUMN "mik_schema"."score_docx"."content3" IS '评语3';
COMMENT ON COLUMN "mik_schema"."score_docx"."score3" IS '评语3分数';
COMMENT ON COLUMN "mik_schema"."score_docx"."score4" IS '综合分数';
COMMENT ON TABLE "mik_schema"."score_docx" IS '成绩单文档模型';

-- ----------------------------
-- Records of score_docx
-- ----------------------------
INSERT INTO "mik_schema"."score_docx" VALUES (1, 1, 'student1', '该学生在毕业设计过程中表现优异，能积极参与讨论，认真完成任务...', 80, '该学生设计思路清晰，实现完整，文档规范，代码结构合理...', 90, '该学生答辩表现良好，回答问题准确，对项目理解深入，能清晰阐述...', 100, 90);
INSERT INTO "mik_schema"."score_docx" VALUES (2, 3, 'student3', '', NULL, '该学生设计思路清晰，实现完整，文档规范，代码结构合理...', 80, '', NULL, NULL);

-- ----------------------------
-- Table structure for scores
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."scores";
CREATE TABLE "mik_schema"."scores" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".scores_id_seq'::regclass),
  "project_title" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "student_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "student_id" int4 NOT NULL,
  "teacher_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "score" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "created_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "update_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp()
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."scores"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."scores"."project_title" IS '项目标题';
COMMENT ON COLUMN "mik_schema"."scores"."student_name" IS '学生姓名';
COMMENT ON COLUMN "mik_schema"."scores"."student_id" IS '学生ID';
COMMENT ON COLUMN "mik_schema"."scores"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "mik_schema"."scores"."score" IS '成绩';
COMMENT ON TABLE "mik_schema"."scores" IS '成绩表，用于记录成绩信息。';

-- ----------------------------
-- Records of scores
-- ----------------------------
INSERT INTO "mik_schema"."scores" VALUES (1, '测试题目1', 'student1', 1, 'teacher1', '80', '2025-03-28 21:03:10.975138+08', '2025-04-04 23:27:49.452618+08');
INSERT INTO "mik_schema"."scores" VALUES (2, '测试题目2', 'student2', 2, 'teacher1', '待评定', '2025-03-30 02:12:09.323134+08', '2025-03-30 02:12:09.323134+08');
INSERT INTO "mik_schema"."scores" VALUES (3, '测试题目3', 'student3', 3, 'teacher1', '待评定', '2025-03-30 11:58:39.478108+08', '2025-03-30 11:58:39.478108+08');

-- ----------------------------
-- Table structure for selections
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."selections";
CREATE TABLE "mik_schema"."selections" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".selections_id_seq'::regclass),
  "username" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "major" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "student_id" int4 NOT NULL,
  "teacher_id" int4 NOT NULL,
  "title" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default" NOT NULL,
  "status" varchar(50) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '待审核'::character varying,
  "created_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "update_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp()
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."selections"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."selections"."username" IS '用户名';
COMMENT ON COLUMN "mik_schema"."selections"."major" IS '专业';
COMMENT ON TABLE "mik_schema"."selections" IS '选题表，用于记录选题信息。';

-- ----------------------------
-- Records of selections
-- ----------------------------
INSERT INTO "mik_schema"."selections" VALUES (1, 'student1', '计算机科学与技术', 1, 1, '测试题目1', '测试题目1描述', '通过', '2025-03-28 21:00:28.643575+08', '2025-03-28 21:03:10.714141+08');
INSERT INTO "mik_schema"."selections" VALUES (2, 'student2', '大数据', 2, 1, '测试题目2', '测试题目描述2', '通过', '2025-03-30 02:10:51.185517+08', '2025-03-30 02:12:09.157366+08');
INSERT INTO "mik_schema"."selections" VALUES (3, 'student3', '软件工程', 3, 1, '测试题目3', '测试题目3描述', '通过', '2025-03-30 11:58:16.27223+08', '2025-03-30 11:58:39.238009+08');

-- ----------------------------
-- Table structure for start_docxs
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."start_docxs";
CREATE TABLE "mik_schema"."start_docxs" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".start_docxs_id_seq'::regclass),
  "mark" varchar(50) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '开题报告'::character varying,
  "title" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "student_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "student_id" int4 NOT NULL,
  "teacher_name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "content1" text COLLATE "pg_catalog"."default" NOT NULL,
  "content2" text COLLATE "pg_catalog"."default" NOT NULL,
  "content3" text COLLATE "pg_catalog"."default" NOT NULL,
  "content4" text COLLATE "pg_catalog"."default" NOT NULL,
  "content5" text COLLATE "pg_catalog"."default" NOT NULL,
  "content6" text COLLATE "pg_catalog"."default" NOT NULL,
  "created_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "update_time" timestamptz(6) NOT NULL DEFAULT pg_systimestamp(),
  "status" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '待审核'::character varying
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."start_docxs"."id" IS '主键';
COMMENT ON COLUMN "mik_schema"."start_docxs"."mark" IS '标记';
COMMENT ON COLUMN "mik_schema"."start_docxs"."title" IS '开题报告标题';
COMMENT ON COLUMN "mik_schema"."start_docxs"."student_name" IS '学生姓名';
COMMENT ON COLUMN "mik_schema"."start_docxs"."student_id" IS '学生ID';
COMMENT ON COLUMN "mik_schema"."start_docxs"."teacher_name" IS '导师姓名';
COMMENT ON COLUMN "mik_schema"."start_docxs"."content1" IS '第一部分内容';
COMMENT ON COLUMN "mik_schema"."start_docxs"."content2" IS '第二部分内容';
COMMENT ON COLUMN "mik_schema"."start_docxs"."content3" IS '第三部分内容';
COMMENT ON COLUMN "mik_schema"."start_docxs"."content4" IS '第四部分内容';
COMMENT ON COLUMN "mik_schema"."start_docxs"."content5" IS '第五部分内容';
COMMENT ON COLUMN "mik_schema"."start_docxs"."content6" IS '第六部分内容';
COMMENT ON COLUMN "mik_schema"."start_docxs"."status" IS '状态';
COMMENT ON TABLE "mik_schema"."start_docxs" IS '开题报告表，用于记录开题报告信息。';

-- ----------------------------
-- Records of start_docxs
-- ----------------------------
INSERT INTO "mik_schema"."start_docxs" VALUES (1, '开题报告', '测试题目3', 'student3', 3, 'teacher1', '待填写11', '待填写11', '待填写11', '待填写11', '待填写11', '待填写', '2025-03-30 11:59:20.264357+08', '2025-03-30 12:03:56.593718+08', '通过');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "mik_schema"."users";
CREATE TABLE "mik_schema"."users" (
  "id" int4 NOT NULL DEFAULT nextval('"mik_schema".users_id_seq'::regclass),
  "username" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "password" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "role" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "student_id" int4,
  "teacher_id" int4,
  "created_time" timestamp(6) DEFAULT pg_systimestamp(),
  "update_time" timestamp(6) DEFAULT pg_systimestamp()
)
WITH (orientation=ROW, storage_type=USTORE)
;
COMMENT ON COLUMN "mik_schema"."users"."id" IS '主键';
COMMENT ON TABLE "mik_schema"."users" IS '用户表，用于记录用户信息。';

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO "mik_schema"."users" VALUES (1, 'student1', '$2b$12$7oLjtOBBT5c5UDe2wu.vbuFb9r/7DhXo15YKRSwvNGduiCFPGFnAC', 'student', 1, 0, '2025-03-20 22:05:22.222476', '2025-03-20 22:05:22.222476');
INSERT INTO "mik_schema"."users" VALUES (2, 'teacher1', '$2b$12$gAML5VrCnwM3BwFkGg9e0.s0wwMfdP9eeSPQslD4biMN3HRsd5YPe', 'teacher', 0, 1, '2025-03-28 20:51:25.079303', '2025-03-28 20:51:25.079303');
INSERT INTO "mik_schema"."users" VALUES (3, 'student2', '$2b$12$zAMG88UGvlOvQVBBF/9BIeAKPj9oi922ELkpnqjVRpPWLRxqkz9c6', 'student', 2, 0, '2025-03-28 21:21:27.586055', '2025-03-28 21:21:27.586055');
INSERT INTO "mik_schema"."users" VALUES (4, 'admin', '$2b$12$olR.iFjWUPP6TTKYX1cGAOfN7FQeXsgXTlf4x9fLGqlaIcdvfX1xS', 'admin', 0, 0, '2025-03-30 01:54:47.435807', '2025-03-30 01:54:47.435807');
INSERT INTO "mik_schema"."users" VALUES (5, 'student3', '$2b$12$TmlPawUyKP0TP8xFV0vbqufRtb6hFfR/sg1v2v7bEDE4Nq3E.GDi2', 'student', 3, 0, '2025-03-30 09:57:53.512515', '2025-03-30 09:57:53.512515');
INSERT INTO "mik_schema"."users" VALUES (6, 'teacher2', '$2b$12$pit1Y35RbuCAZFODmnrrJug6.n3zQ35dQJGr4bJCA3LpkAIWT9Gra', 'teacher', 0, 3, '2025-03-30 09:58:34.760703', '2025-03-30 09:58:34.760703');
INSERT INTO "mik_schema"."users" VALUES (7, 'teacher3', '$2b$12$WROwoXc3MsOzEUgHfaWxse2M5/O1xGsik0UhPTGRLT4irIX/yJNci', 'teacher', 0, 3, '2025-04-05 01:46:32.750227', '2025-04-05 01:46:32.750227');

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."aerich_id_seq"
OWNED BY "mik_schema"."aerich"."id";
SELECT setval('"mik_schema"."aerich_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."defenses_id_seq"
OWNED BY "mik_schema"."defenses"."id";
SELECT setval('"mik_schema"."defenses_id_seq"', 9, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."end_docxs_id_seq"
OWNED BY "mik_schema"."end_docxs"."id";
SELECT setval('"mik_schema"."end_docxs_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."groups_id_seq"
OWNED BY "mik_schema"."groups"."id";
SELECT setval('"mik_schema"."groups_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."middle_docxs_id_seq"
OWNED BY "mik_schema"."middle_docxs"."id";
SELECT setval('"mik_schema"."middle_docxs_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."phase_id_seq"
OWNED BY "mik_schema"."phase"."id";
SELECT setval('"mik_schema"."phase_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."projects_id_seq"
OWNED BY "mik_schema"."projects"."id";
SELECT setval('"mik_schema"."projects_id_seq"', 3, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."score_docx_id_seq"
OWNED BY "mik_schema"."score_docx"."id";
SELECT setval('"mik_schema"."score_docx_id_seq"', 2, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."scores_id_seq"
OWNED BY "mik_schema"."scores"."id";
SELECT setval('"mik_schema"."scores_id_seq"', 3, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."selections_id_seq"
OWNED BY "mik_schema"."selections"."id";
SELECT setval('"mik_schema"."selections_id_seq"', 3, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."start_docxs_id_seq"
OWNED BY "mik_schema"."start_docxs"."id";
SELECT setval('"mik_schema"."start_docxs_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "mik_schema"."users_id_seq"
OWNED BY "mik_schema"."users"."id";
SELECT setval('"mik_schema"."users_id_seq"', 7, true);

-- ----------------------------
-- Primary Key structure for table aerich
-- ----------------------------
ALTER TABLE "mik_schema"."aerich" ADD CONSTRAINT "aerich_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table defenses
-- ----------------------------
ALTER TABLE "mik_schema"."defenses" ADD CONSTRAINT "defenses_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table end_docxs
-- ----------------------------
ALTER TABLE "mik_schema"."end_docxs" ADD CONSTRAINT "end_docxs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table groups
-- ----------------------------
ALTER TABLE "mik_schema"."groups" ADD CONSTRAINT "groups_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table middle_docxs
-- ----------------------------
ALTER TABLE "mik_schema"."middle_docxs" ADD CONSTRAINT "middle_docxs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table phase
-- ----------------------------
ALTER TABLE "mik_schema"."phase" ADD CONSTRAINT "phase_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table projects
-- ----------------------------
ALTER TABLE "mik_schema"."projects" ADD CONSTRAINT "projects_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table score_docx
-- ----------------------------
ALTER TABLE "mik_schema"."score_docx" ADD CONSTRAINT "score_docx_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table scores
-- ----------------------------
ALTER TABLE "mik_schema"."scores" ADD CONSTRAINT "scores_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table selections
-- ----------------------------
ALTER TABLE "mik_schema"."selections" ADD CONSTRAINT "selections_username_key" UNIQUE ("username");

-- ----------------------------
-- Primary Key structure for table selections
-- ----------------------------
ALTER TABLE "mik_schema"."selections" ADD CONSTRAINT "selections_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table start_docxs
-- ----------------------------
ALTER TABLE "mik_schema"."start_docxs" ADD CONSTRAINT "start_docxs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table users
-- ----------------------------
ALTER TABLE "mik_schema"."users" ADD CONSTRAINT "users_username_key" UNIQUE ("username");

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "mik_schema"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");
