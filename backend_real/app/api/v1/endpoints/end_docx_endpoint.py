from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import FileResponse
from datetime import datetime

from app.models.project import Project

from app.models.end_docx import EndDocx
from app.schemas.end_docx import EndDocxModel, EndDocxIn, EndDocxOut, EndDocxDetail, EndDocxUpdateStatus
from utlis.end_docx import replace_text_in_docx
import os


router = APIRouter()

# 学生创建结题报告
@router.post("/student/create/", response_model=EndDocxOut, summary="学生创建结题报告", description="描述详细接口XXXX", responses={200: {"描述": "结题报告创建成功"}})
async def create_end_docx_endpoint(end_docx: EndDocxIn):
    end_docx_obj = await EndDocx.create(**end_docx.dict())

    # 获取项目根目录
    project_root = 'D:\\Code\\GPMS\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(end_docx.student_id), 'end_docx')
    os.makedirs(output_dir, exist_ok=True)

    input_file = os.path.join(project_root, 'template', '任务书_模板.docx')

    output_path = os.path.join(output_dir, f'{end_docx.student_id}_结题报告.docx')
    print(f"Output path: {output_path}")

    # 调用函数替换word文本
    replacements = {
        "{学生姓名}": str(end_docx.student_id),
        "{专业班级}": "软件工程2025级1班",
        "{题目}": end_docx.title,
        "{学院}": "计算机",
        "{指导教师}": end_docx.teacher_name,
        "{content1}": end_docx.content1,
        "{content2}": end_docx.content2,
        "{content3}": end_docx.content3,
        "{content4}": end_docx.content4,
    }

    replace_text_in_docx(input_file, output_path, replacements)

    return EndDocxOut.from_orm(end_docx_obj)


# 下载结题报告word文档
@router.get("/student/download/{student_id}", summary="下载结题报告word文档")
async def download_end_docx(student_id: int):
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'end_docx')
    file_path = os.path.join(output_dir, f'{student_id}_结题报告.docx')

    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文件不存在")

    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f'{student_id}_结题报告.docx')


# 根据username获取这个教师管理的学生的所有结题报告
@router.get("/teacher/{username}", response_model=list[EndDocxOut], summary="教师查询结题报告", status_code=status.HTTP_200_OK)
async def get_end_docx(username: str):
    end_docxs = await EndDocx.filter(teacher_name=username).all()
    return [EndDocxOut.from_orm(end_docx) for end_docx in end_docxs]


# 根据student_id获取学生的结题报告详情
@router.get("/teacher/detail/{student_id}", response_model=EndDocxDetail, summary="教师查询结题报告", status_code=status.HTTP_200_OK)
async def get_end_docx_detail(student_id: int):
    end_docx = await EndDocx.filter(student_id=student_id).first()
    if not end_docx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="结题报告不存在")
    return EndDocxDetail.model_validate(end_docx)


# 教师根据student_id修改结题报告状态，当接收到的状态为"通过"时，更新当前学生的的项目状态为：通过结题报告；并生成word文档
@router.put("/teacher/{student_id}", response_model=EndDocxOut, summary="教师更新结题报告状态", status_code=status.HTTP_200_OK)
async def update_end_docx_status(student_id: int, end_docx: EndDocxUpdateStatus):
    await EndDocx.filter(student_id=student_id).update(status=end_docx.status, update_time=datetime.now())
    end_docx_obj = await EndDocx.filter(student_id=student_id).first()
    if not end_docx_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="结题报告不存在")

    # 如果状态为通过，则更新项目状态
    if end_docx.status == "通过":
        await Project.filter(student_id=student_id).update(status="结题", update_time=datetime.now())

    return EndDocxOut.from_orm(end_docx_obj)














