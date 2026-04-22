import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

OPTIMIZED_PROMPT = """
你是一位专业的B端客户成功经理，擅长处理客户沟通与危机公关。请根据以下要求，撰写一封给企业客户的正式道歉邮件： <context> - 客户公司名称：[客户公司] - 问题产品：SaaS数据分析平台 - 问题描述：昨日系统更新后，部分用户的实时数据看板出现约3小时的数据延迟 - 影响范围：约15%的企业客户受影响 </context> <requirements> 1. **语气风格**：专业、诚恳、冷静，承认错误但避免过度道歉（如“深感愧疚”等情绪化表述）。 2. **邮件结构**：    - 标题：清晰说明主题    - 第一段：直接说明问题并致歉    - 第二段：简要说明原因（技术层面，非借口）    - 第三段：具体补救措施（分点列出）    - 第四段：预防措施与后续改进    - 结尾：引导客户下一步行动（如确认解决、提供反馈渠道） 3. **关键要素**：    - 必须包含补偿方案（如延长7天服务期）    - 必须提供技术负责人联系方式    - 避免使用“我们很遗憾”等被动表述，改用“我们已立即修复” 4. **格式要求**：使用专业邮件格式，段落清晰，长度在200-300字。 </requirements> <example> 标题：关于数据看板延迟问题的说明与致歉 尊敬的[客户公司]团队： 我们获悉，昨日（10月26日）下午2点至5点期间，部分用户的实时数据看板出现了数据延迟。对于由此给您工作带来的不便，我们真诚致歉。 经技术团队排查，此问题源于系统更新时的一个配置异常，导致部分数据流处理延迟。问题发生后，我们立即启动应急预案，已于昨日下午5点15分完全修复。 为弥补此次影响，我们将采取以下措施： 1. 为您的账户延长7天服务期，自动生效。 2. 提供受影响时段的完整数据补偿报告，明日发送至您的账户。 3. 设立专项技术支持通道，技术负责人张工（zhang@company.com）将直接跟进后续问题。 我们已优化更新流程，增加双重验证机制，防止类似问题再次发生。 请您登录平台确认数据已恢复正常。如有任何疑问，可随时联系张工或您的客户经理。感谢您的理解与支持。 此致 敬礼 [你的姓名] 客户成功总监 ABC科技公司 </example> 请基于以上要求，撰写完整的道歉邮件。如信息不足，可合理假设并注明。
"""

ORIGINAL_PROMPT = "你帮我写一个邮件给客户道歉因为我们的产品出现了bug。"

def call(prompt):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500
    )
    return resp.choices[0].message.content

print("=" * 60)
print("📧 原版 Prompt 输出")
print("=" * 60)
print(call(ORIGINAL_PROMPT))

print("\n" + "=" * 60)
print("📧 优化版 Prompt 输出")
print("=" * 60)
print(call(OPTIMIZED_PROMPT))