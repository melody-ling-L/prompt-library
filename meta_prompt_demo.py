import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# 故意用一个"烂"Prompt
MY_BAD_PROMPT = """你帮我写一个邮件给客户道歉因为我们的产品出现了bug。"""

META_PROMPT = f"""你是一个有5年经验的 Prompt Engineering 专家，熟悉 Anthropic 和 OpenAI 官方指南。

我的任务目标：
让大模型生成一封 B 端客户道歉邮件，要求：
- 承认错误但不过度自责
- 包含具体的补救措施
- 保持专业语气
- 结尾引导客户下一步行动

我当前的 Prompt（效果不好）：
<current_prompt>
{MY_BAD_PROMPT}
</current_prompt>

请：
1. 指出这个 Prompt 的 3 个主要问题
2. 基于 Anthropic 官方 Prompt 工程最佳实践（Role / XML / Few-shot / Constraint）重写一版
3. 解释每个改动的原因

输出格式：
## 问题诊断
1. ...
2. ...
3. ...

## 优化后的 Prompt
<优化后的完整 Prompt>
## 改动说明
- 改动1：XXX，因为YYY
- 改动2：...
- 改动3：..."""

def main():
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": META_PROMPT}],
        temperature=0.3,
        max_tokens=2000
    )
    print(resp.choices[0].message.content)

if __name__ == "__main__":
    main()