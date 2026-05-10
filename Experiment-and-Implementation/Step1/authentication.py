from typing import TypedDict, Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama  # 🌟 换成 Ollama 专属模块
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('MODELSCOPE_SDK_TOKEN')

# ==========================================
# 1. 定义全局状态 (State) 
# ==========================================
class CaseState(TypedDict, total=False):
    raw_materials: str
    client_info: Dict[str, Any]
    auth_docs: Dict[str, str]

# ==========================================
# 2. 定义 Pydantic 数据模型 (Schema)
# ==========================================
class ClientInfo(BaseModel):
    plaintiff_name: str = Field(description="原告姓名或原告公司名称。如果未找到，填'未知'")
    plaintiff_id: str = Field(description="原告身份证号或统一社会信用代码。如果未找到，填'未知'")
    defendant_name: str = Field(description="被告姓名或被告公司名称。如果未找到，填'未知'")
    jurisdiction: str = Field(description="管辖地或案件发生地。如果未找到，填'未知'")

# ==========================================
# 3. 节点逻辑：Step 1 处理函数
# ==========================================
def step1_intake(state: CaseState) -> CaseState:
    print("\n🚀 [Step 1] 开始执行: 准入与授权 MS - Deepseek...")
    raw_text = state.get("raw_materials", "")
    if not raw_text:
        raise ValueError("原始材料为空，无法执行 Step 1")

    # 3.1 🌟 初始化本地 Ollama 模型
    llm = ChatOpenAI(
        model="deepseek-ai/DeepSeek-V4-Flash",  # 👈 请一字不差地复制这个名字
        api_key=api_key,
        base_url="https://api-inference.modelscope.cn/v1",
        temperature=0.1, 
    )

    # 3.2 初始化 JSON 解析器
    parser = JsonOutputParser(pydantic_object=ClientInfo)

    # 3.3 构建 Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个严谨的法律助理。请从提供的OCR客户材料中精确提取原被告信息。直接输出JSON，不要包含任何其他文字。\n\n{format_instructions}"),
        ("human", "客户原始材料如下：\n{raw_text}")
    ])

    # 3.4 执行抽取链
    chain = prompt | llm | parser

    print("⏳ Deepseek 提取核心信息...")
    
    try:
        # 传入格式化指令
        extracted_dict = chain.invoke({
            "raw_text": raw_text,
            "format_instructions": parser.get_format_instructions()
        })
        
        # 验证提取结果
        extracted_info = ClientInfo(**extracted_dict)
        print(f"✅ 本地提取成功: {extracted_info.model_dump()}")

        # 3.5 渲染本地模板
        auth_template = """
========================================
             【授权委托书】             

委托人：{plaintiff_name} 
证件号码：{plaintiff_id}

受委托人：Agent 虚拟律师事务所 律师

    现委托上述受委托人在我方与 {defendant_name} 的纠纷一案中，作为我方的一审诉讼代理人。
    代理权限为：特别授权（包括但不限于代为承认、放弃、变更诉讼请求，进行和解，提起反诉或者上诉等）。

                                委托人（签字/盖章）：_____________
                                日期：____年__月__日
========================================
"""
        
        filled_doc = auth_template.format(**extracted_info.model_dump())

        return {
            "client_info": extracted_info.model_dump(),
            "auth_docs": {"授权委托书": filled_doc}
        }
        
    except Exception as e:
        print(f"❌ 本地解析失败: {e}")
        raise e

# ==========================================
# 4. 测试运行模块
# ==========================================
if __name__ == "__main__":
    # 模拟一份客户发来的材料
    mock_raw_materials = """
    律师你好，我要起诉。我是张三，身份证号是 110105199001018888。
    对面那个欠钱不还的公司叫“深圳市南山小李贸易有限公司”。
    事情发生在深圳南山区。麻烦帮我弄一下委托书。
    """
    
    initial_state: CaseState = {"raw_materials": mock_raw_materials}
    new_state = step1_intake(initial_state)
    print("\n📄 最终生成的案卷内容：\n", new_state["auth_docs"]["授权委托书"])