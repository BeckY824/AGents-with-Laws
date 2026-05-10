import os
import requests
import json
from dotenv import load_dotenv

# 1. 加载环境变量中的 Token
load_dotenv()
api_key = os.getenv('MODELSCOPE_SDK_TOKEN')

if not api_key:
    print("❌ 找不到 MODELSCOPE_SDK_TOKEN，请检查 .env 文件！")
    exit()

# 2. 构造最底层的 HTTP 请求
url = "https://api-inference.modelscope.cn/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# ⚠️ 注意：这里使用脱敏的测试文本，避免触发平台的隐私拦截导致返回空数据
test_prompt = """
请提取以下文本中的人物和地点信息，输出JSON格式：
我是李四，身份证号 44030519990101XXXX。昨天在深圳市南山区发生了纠纷。
"""

payload = {
    "model": "deepseek-ai/DeepSeek-V4-Flash",  # 你想探测的那个模型 ID
    "messages": [{"role": "user", "content": test_prompt}],
    "temperature": 0.1
}

print(f"🚀 正在向 ModelScope 发送底层请求...")
print(f"📦 目标模型: {payload['model']}\n")

try:
    # 3. 发送请求
    response = requests.post(url, headers=headers, json=payload)
    
    # 4. 打印最真实的 HTTP 状态
    print("="*40)
    print(f"📡 HTTP 状态码: {response.status_code}")
    print("="*40)
    
    # 5. 尝试解析并打印优美的 JSON
    try:
        raw_json = response.json()
        print("📥 服务器返回的完整 JSON 结构 (Raw Output):\n")
        print(json.dumps(raw_json, indent=4, ensure_ascii=False))
        
        # 简单诊断
        print("\n" + "="*40)
        print("🔍 结构诊断报告:")
        if "choices" in raw_json:
            if raw_json["choices"] is None:
                print("❌ 致命缺陷: 包含 'choices' 键，但其值为 null (这就是导致 LangChain 崩溃的真凶！)")
            elif len(raw_json["choices"]) == 0:
                print("❌ 致命缺陷: 'choices' 是一个空列表 [] (可能是触发了平台安全拦截)")
            else:
                print("✅ 'choices' 字段看起来正常，包含数据。")
        elif "output" in raw_json:
             print("⚠️ 警告: 发现非标结构！内容似乎藏在 'output' 字段中，而不是标准的 'choices' 中。")
        elif "error" in raw_json:
             print(f"❌ 明确报错: 平台返回了错误信息 -> {raw_json['error'].get('message', '未知错误')}")
        else:
             print("❓ 极其罕见的结构，完全不符合 OpenAI 标准协议。")
             
    except json.JSONDecodeError:
        print("❌ 服务器返回的不是合法的 JSON 格式！原始返回文本如下：")
        print(response.text)

except Exception as e:
    print(f"❌ 请求发生网络或代码级错误: {e}")