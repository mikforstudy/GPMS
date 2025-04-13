from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import FileResponse
from datetime import datetime
from pydantic import BaseModel

from app.models.project import Project
from app.models.start_docx import StartDocx
from app.schemas.start_docx import StartDocxModel, StartDocxIn, StartDocxOut, StartDocxDetail, StartDocxUpdateStatus
from utlis.start_docx import create_start_docx
import os

router = APIRouter()

# 学生创建开题报告
@router.post("/student/create/", response_model=StartDocxOut, summary="学生创建开题报告", description="描述详细接口XXXX", responses={200: {"描述": "开题报告创建成功"}})
async def create_start_docx_endpoint(start_docx: StartDocxIn):
    start_docx_obj = await StartDocx.create(**start_docx.dict())

    # 获取项目根目录
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output',str(start_docx.student_id), 'start_docx')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f'{start_docx.student_id}_开题报告.docx')
    print(f"Output path: {output_path}")

    # 调用函数创建 Word 文档
    create_start_docx(
        title=start_docx.title,
        teacher_name=start_docx.teacher_name,
        student_name=start_docx.student_name,
        student_id=str(start_docx.student_id),
        content1=start_docx.content1,
        content2=start_docx.content2,
        content3=start_docx.content3,
        content4=start_docx.content4,
        content5=start_docx.content5,
        content6=start_docx.content6,
        output_path=os.path.join(output_dir, f'{start_docx.student_id}_开题报告.docx')
    )

    return start_docx_obj


# 下载开题报告word文档
@router.get("/student/download/{student_id}", summary="下载开题报告word文档")
async def download_start_docx(student_id: int):
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'start_docx')
    file_path = os.path.join(output_dir, f'{student_id}_开题报告.docx')

    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文件不存在")

    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f'{student_id}_开题报告.docx')


# 根据username获取这个教师管理的学生的所有开题报告
@router.get("/teacher/{username}", response_model=list[StartDocxOut], summary="教师查询开题报告", status_code=status.HTTP_200_OK)
async def get_start_docx(username: str):
    start_docxs = await StartDocx.filter(teacher_name=username).all()
    return [StartDocxOut.from_orm(start_docx) for start_docx in start_docxs]


# 根据student_id获取学生的开题报告详情
@router.get("/teacher/detail/{student_id}", response_model=StartDocxDetail, summary="教师查询开题报告详情", status_code=status.HTTP_200_OK)
async def get_start_docx(student_id: int):
    start_docx = await StartDocx.filter(student_id=student_id).first()
    if not start_docx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="开题报告不存在")
    return StartDocxDetail.from_orm(start_docx)


# 教师根据student_id修改开题报告状态和content6；# 当接收到的状态为"通过"时，更新当前学生的的项目状态为：通过开题报告；并生成word文档
@router.put("/teacher/{student_id}", response_model=StartDocxOut, summary="教师修改开题报告状态", status_code=status.HTTP_200_OK)
async def update_start_docx_status(student_id: int, start_docx: StartDocxUpdateStatus):
    await StartDocx.filter(student_id=student_id).update(status=start_docx.status, content6=start_docx.content6, update_time=datetime.now())
    start_docx_obj = await StartDocx.filter(student_id=student_id).first()
    if not start_docx_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="开题报告不存在")

    # 当接收到的状态为"通过"时，更新当前学生的的项目状态为：通过开题报告
    if start_docx.status == "通过":
        project = await Project.filter(student_id=student_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
        await Project.filter(student_id=student_id).update(status="通过开题报告", update_time=datetime.now())

    # 获取项目根目录
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'start_docx')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f'{student_id}_开题报告.docx')
    print(f"Output path: {output_path}")

    # 调用函数创建 Word 文档
    create_start_docx(
        title=start_docx_obj.title,
        teacher_name=start_docx_obj.teacher_name,
        student_name=start_docx_obj.student_name,
        student_id=str(start_docx_obj.student_id),
        content1=start_docx_obj.content1,
        content2=start_docx_obj.content2,
        content3=start_docx_obj.content3,
        content4=start_docx_obj.content4,
        content5=start_docx_obj.content5,
        content6=start_docx_obj.content6,
        output_path=os.path.join(output_dir, f'{student_id}_开题报告.docx')
    )

    return StartDocxOut.from_orm(start_docx_obj)
