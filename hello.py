import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个专业的 Prompt Engineer 教练。"},
        {"role": "user", "content": """你是一个招聘过 50+ Prompt Engineer 的技术总监。
基于我对岗位 JD 的理解，Prompt Engineer 的核心能力应该包括：
1. Prompt 设计方法论
2. 评测体系构建
3. 模型选型判断
4. 工程化落地
5. 业务价值转化

请从这 5 个维度，告诉我哪个是最核心的"分水岭能力"——即区分普通候选人和优秀候选人的那一项？为什么？200 字以内。"""}
    ],
    temperature=0.2
)

print("=" * 50)
print("模型回复：")
print(response.choices[0].message.content)
print("=" * 50)
print(f"输入 tokens: {response.usage.prompt_tokens}")
print(f"输出 tokens: {response.usage.completion_tokens}")
print(f"总计 tokens: {response.usage.total_tokens}")