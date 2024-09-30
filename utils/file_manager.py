# file_manager.py

import os
import http.client
import json

ALIST_URL = "warehouse.archknowledge.com.cn"
ALIST_AUTHORIZATION = "alist-79f0737a-97a0-4c5f-a51e-df4afecd5d44dB1P9QSM5FRCJbUc0HrywajGijam55RFS1hSvLCGLviwwGhsoqtcaGGcByeg7ELM"

def fetch_file_list_from_alist(path):
    """
    从 Alist API 获取文件列表。

    Args:
        path (str): 要获取的目录路径。

    Returns:
        list: 文件和文件夹结构列表。
    """
    conn = http.client.HTTPConnection(ALIST_URL)
    payload = json.dumps({"path": path, "password": "", "page": 1, "per_page": 0, "refresh": False})
    headers = {
        'Authorization': ALIST_AUTHORIZATION,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/fs/list", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    
    if data['code'] == 200:
        return data['data']['content']
    else:
        return []

def get_current_path():
    """
    获取当前文件所在路径。

    Returns:
        str: 当前文件所在的绝对路径。
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
