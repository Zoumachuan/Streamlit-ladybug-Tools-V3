# data_loader.py
import zipfile
import tempfile
from ladybug.epw import EPW

def load_epw_file(file_path):
    """
    加载指定路径的EPW文件。

    Args:
        file_path (str): EPW文件的路径。

    Returns:
        EPW: 加载的EPW对象。
    """
    return EPW(file_path)

def unzip_and_load_epw(zip_file_path, selected_zip_file):
    """
    解压缩ZIP文件，并加载选中的EPW文件。

    Args:
        zip_file_path (str): ZIP文件的路径。
        selected_zip_file (str): 选中的ZIP文件名。

    Returns:
        EPW: 加载的EPW对象。
    """
    # 打开本地ZIP文件
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        # 确保选中的 EPW 文件名相对于 ZIP 文件的名称
        epw_file_name = selected_zip_file.replace('.zip', '.epw')

        # 读取选中的EPW文件数据
        epw_data = zip_ref.read(epw_file_name)

        # 保存解压后的EPW数据到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epw") as temp_file:
            temp_file.write(epw_data)
            temp_file_path = temp_file.name
    # 加载解压后的EPW文件
    return EPW(temp_file_path)

def load_uploaded_epw(uploaded_file):
    """
    加载用户上传的EPW文件。

    Args:
        uploaded_file (UploadedFile): 上传的EPW文件对象。

    Returns:
        EPW: 加载的EPW对象。
    """
    # 读取上传的EPW文件数据
    epw_data = uploaded_file.read()

    # 保存上传的EPW数据到临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epw") as temp_file:
        temp_file.write(epw_data)
        temp_file_path = temp_file.name

    # 加载上传的EPW文件
    return EPW(temp_file_path)
