import zipfile
import tempfile
import os
import shutil
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse


router = APIRouter()

# 学生根据学生id导出所有文件的压缩包
@router.get("/student/{student_id}", summary="学生导出文件", status_code=200)
async def export_files(student_id: int):
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id))
    print(output_dir)
    # 检查目录是否存在
    if not os.path.exists(output_dir):
        raise HTTPException(status_code=404, detail="目录不存在")

    # 创建临时文件用于保存压缩包
    temp_dir = tempfile.mkdtemp()
    zip_filename = f"student_{student_id}_files.zip"
    zip_filepath = os.path.join(temp_dir, zip_filename)

    try:
        # 创建压缩文件
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历目录中的所有文件和子目录
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 获取相对路径，保持目录结构
                    rel_path = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, rel_path)

        # 返回压缩文件
        response = FileResponse(
            zip_filepath,
            media_type="application/zip",
            filename=zip_filename
        )

        # 创建临时文件清理函数
        async def cleanup_temp_dir():
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"清理临时目录出错: {str(e)}")

        # 设置响应处理结束后的回调函数
        response.background = cleanup_temp_dir
        return response
    except Exception as e:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"压缩文件时出错: {str(e)}")


# 教师根据学生id导出所有文件的压缩包
@router.get("/teacher/{student_id}", summary="教师导出文件", status_code=200)
async def export_files(student_id: int):
    project_root = 'D:\\Code\\demo\\backend_real'
    output_dir = os.path.join(project_root, 'output', str(student_id))
    print(output_dir)
    # 检查目录是否存在
    if not os.path.exists(output_dir):
        raise HTTPException(status_code=404, detail="目录不存在")

    # 创建临时文件用于保存压缩包
    temp_dir = tempfile.mkdtemp()
    zip_filename = f"teacher_{student_id}_files.zip"
    zip_filepath = os.path.join(temp_dir, zip_filename)

    try:
        # 创建压缩文件
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历目录中的所有文件和子目录
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 获取相对路径，保持目录结构
                    rel_path = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, rel_path)

        # 返回压缩文件
        response = FileResponse(
            zip_filepath,
            media_type="application/zip",
            filename=zip_filename
        )

        # 创建临时文件清理函数
        async def cleanup_temp_dir():
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                print(f"清理临时目录出错: {str(e)}")

        # 设置响应处理结束后的回调函数
        response.background = cleanup_temp_dir
        return response
    except Exception as e:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"压缩文件时出错: {str(e)}")