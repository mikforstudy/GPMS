from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import FileResponse
from datetime import datetime

from app.models.project import Project

from app.models.middle_docx import MiddleDocx
from app.schemas.middle_docx import MiddleDocxModel, MiddleDocxIn, MiddleDocxOut, MiddleDocxDetail, MiddleDocxUpdateStatus
from utlis.middle_docx import create_middle_docx
import os

router = APIRouter()

# 学生创建中期报告
@router.post("/student/create/", response_model=MiddleDocxOut, summary="学生创建中期报告", description="描述详细接口XXXX", responses={200: {"描述": "中期报告创建成功"}})
async def create_middle_docx_endpoint(middle_docx: MiddleDocxIn):
    middle_docx_obj = await MiddleDocx.create(**middle_docx.dict())

    # 获取项目根目录
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(middle_docx.student_id), 'middle_docx')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f'{middle_docx.student_id}_中期报告.docx')
    print(f"Output path: {output_path}")

    # 调用函数创建 Word 文档
    create_middle_docx(
        title=middle_docx.title,
        teacher_name=middle_docx.teacher_name,
        student_name=middle_docx.student_name,
        student_id=str(middle_docx.student_id),
        content1=middle_docx.content1,
        content6=middle_docx.content6,
        content7=middle_docx.content7,
        output_path=os.path.join(output_dir, f'{middle_docx.student_id}_中期报告.docx')
    )

    return middle_docx_obj


# 下载中期报告word文档
@router.get("/student/download/{student_id}", summary="下载中期报告word文档")
async def download_middle_docx(student_id: int):
    project_root = 'D:\\Code\\GPMS\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'middle_docx')
    file_path = os.path.join(output_dir, f'{student_id}_中期报告.docx')

    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文件不存在")

    return FileResponse(file_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=f'{student_id}_中期报告.docx')


# 根据username获取这个教师管理的学生的所有中期检查报告
@router.get("/teacher/{username}", response_model=list[MiddleDocxOut], summary="教师查询中期报告", status_code=status.HTTP_200_OK)
async def get_middle_docx(username: str):
    middle_docxs = await MiddleDocx.filter(teacher_name=username).all()
    return [MiddleDocxOut.from_orm(middle_docx) for middle_docx in middle_docxs]

# 根据student_id获取学生的中期检查详情
@router.get("/teacher/detail/{student_id}", response_model=MiddleDocxDetail, summary="教师查询中期报告", status_code=status.HTTP_200_OK)
async def get_middle_docx_detail(student_id: int):
    middle_docx = await MiddleDocx.filter(student_id=student_id).first()
    if not middle_docx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="中期报告不存在")
    return MiddleDocxDetail.model_validate(middle_docx)


# 教师根据student_id修改中期检查状态，当接收到的状态为"通过"时，更新当前学生的的项目状态为：通过中期检查；和content6；并生成word文档
@router.put("/teacher/{student_id}", response_model=MiddleDocxOut, summary="教师更新中期报告状态", status_code=status.HTTP_200_OK)
async def update_middle_docx_status(student_id: int, middle_docx: MiddleDocxUpdateStatus):
    await MiddleDocx.filter(student_id=student_id).update(status=middle_docx.status, content6=middle_docx.content6, update_time=datetime.now())
    middle_docx_obj = await MiddleDocx.filter(student_id=student_id).first()
    if not middle_docx_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="中期报告不存在")

    # 当接收到的状态为"通过"时，更新当前学生的的项目状态为：通过中期检查
    if middle_docx.status == "通过":
        project = await Project.filter(student_id=student_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
        await Project.filter(student_id=student_id).update(status="通过中期检查", update_time=datetime.now())

    # 获取项目根目录
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'middle_docx')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f'{student_id}_中期报告.docx')
    print(output_path)

    # 调用函数创建 Word 文档
    create_middle_docx(
        title=middle_docx_obj.title,
        teacher_name=middle_docx_obj.teacher_name,
        student_name=middle_docx_obj.student_name,
        student_id=str(middle_docx_obj.student_id),
        content1=middle_docx_obj.content1,
        content6=middle_docx_obj.content6,
        content7=middle_docx_obj.content7,
        output_path=os.path.join(output_dir, f'{middle_docx_obj.student_id}_中期报告.docx')
    )

    return MiddleDocxOut.from_orm(middle_docx_obj)

