import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('MODELSCOPE_SDK_TOKEN')

url = "https://api-inference.modelscope.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    # 测试当前的模型 ID 是否有效
    "model": "ZhipuAI/GLM-5.1", 
    "messages": [{"role": "user", "content": "你好"}]
}

print("正在发送请求到 ModelScope...")
response = requests.post(url, headers=headers, json=data)

# 打印最真实的返回结果
print("HTTP 状态码:", response.status_code)
print("服务器真实返回:", response.json())