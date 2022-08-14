import os
from dotenv import load_dotenv

# 自动搜索.env文件
load_dotenv(verbose=True)

def get_string(key: str):
    if not key or type(key) is not str:
        return None
    return os.getenv(key) or None