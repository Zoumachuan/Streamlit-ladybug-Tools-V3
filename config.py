import os

# 从环境变量中读取 OpenAI API 的协议、主机和密钥
OPENAI_API_SCHEME = os.getenv('OPENAI_API_SCHEME')
OPENAI_API_HOST = os.getenv('OPENAI_API_HOST')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_api_credentials():
    """
    返回 OpenAI API 的协议、主机和密钥。

    Returns:
        tuple: OpenAI API 的协议、主机和密钥
    """
    return OPENAI_API_SCHEME, OPENAI_API_HOST, OPENAI_API_KEY
