from fastapi import FastAPI, File, UploadFile
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.models.project import Project
from app.models.user import User
import os
import datetime


router = APIRouter()
# 上传过程文档文件，传入student_id和文件【可以上传多个文件】
@router.post("/upload/{student_id}" , summary="上传过程文档文件", description="上传过程文档文件")
async def upload_process_file(student_id: int, files: list[UploadFile] = File(...)):
    project_root = 'D:\\Code\\GPMS\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'process')
    os.makedirs(output_dir, exist_ok=True)

    for file in files:
        file_path = os.path.join(output_dir, f'{file.filename}')
        with open(file_path, 'wb') as f:
            f.write(file.file.read())

    return {"message": "文件上传成功"}


# 根据student_id获取过程文档文件列表，并返回文件大小和创建时间
@router.get("/list/{student_id}" , summary="获取过程文档文件列表", description="获取过程文档文件列表")
async def list_process_file(student_id: int):
    project_root = 'D:\\Code\\GPMS\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'process')
    if os.path.exists(output_dir):
        file_list = []
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            file_size = os.path.getsize(file_path)
            file_ctime = os.path.getctime(file_path)
            file_list.append({"file_name": file, "file_size": file_size, "file_ctime": file_ctime})
        return file_list
    else:
        raise HTTPException(status_code=404, detail="文件夹不存在")

# 根据student_id和文件名删除过程文档文件
@router.delete("/delete/{student_id}" , summary="删除过程文档文件", description="删除过程文档文件")
async def delete_process_file(student_id: int, file_name: str):
    project_root = 'D:\\Code\\GPMS\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id), 'process')
    file_path = os.path.join(output_dir, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "文件删除成功"}
    else:
        raise HTTPException(status_code=404, detail="文件不存在")


# 教师：在projects表里根据teacher_name查询student_id，然后根据student_id查询每个学生过程文档文件，返回文件信息
@router.get("/teacher/{teacher_name}", summary="教师查询过程文档文件", description="教师查询过程文档文件")
async def get_teacher_process_files(teacher_name: str):
    # 1. 根据teacher_name查询所有相关的项目
    projects = await Project.filter(teacher_name=teacher_name).all()
    if not projects:
        raise HTTPException(status_code=404, detail="没有找到该教师指导的项目")

    # 2. 收集所有学生的过程文档
    result = []
    project_root = 'D:\\Code\\GPMS\\backend_real'

    for project in projects:
        student_id = project.student_id
        queryset = await User.filter(student_id=student_id).first()
        student_name = queryset.username
        student_files = []

        # 检查该学生的过程文档目录
        output_dir = os.path.join(project_root, 'output', str(student_id), 'process')
        if os.path.exists(output_dir):
            # 收集文件信息
            for file in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file)
                file_size = os.path.getsize(file_path)
                file_ctime = os.path.getctime(file_path)
                creation_time = datetime.datetime.fromtimestamp(file_ctime).strftime('%Y-%m-%d %H:%M:%S')
                file_size_kb = round(file_size / 1024, 2)

                student_files.append({
                    "file_name": file,
                    "file_size": f"{file_size_kb} KB",
                    "file_ctime": creation_time,
                    "download_url": f"/api/v1/process/teacher/download/{teacher_name}/{student_id}/{file}"
                })

        # 添加到结果中
        result.append({
            "student_id": student_id,
            "student_name": student_name,
            "title": project.title,
            "files": student_files
        })

    return result


# 教师下载学生的过程文档文件
@router.get("/teacher/download/{teacher_name}/{student_id}/{file_name}", summary="教师下载学生过程文档",
            description="教师下载指定学生的过程文档文件")
async def download_student_process_file(teacher_name: str, student_id: int, file_name: str):
    # 1. 验证学生是否是该教师指导的
    project = await Project.filter(teacher_name=teacher_name, student_id=student_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限访问该学生的文件"
        )

    # 2. 构建文件路径并检查文件是否存在
    project_root = 'D:\\Code\\GPMS\\backend_real'
    file_path = os.path.join(project_root, 'output', str(student_id), 'process', file_name)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    # 3. 返回文件响应
    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type='application/octet-stream'  # 使用通用MIME类型，浏览器会根据文件扩展名判断
    )



