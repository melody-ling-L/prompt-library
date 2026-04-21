import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# 跟昨天一样的 10 条测试集
TEST_SET = [
    {"text": "这个快递真是'神速'，我从下单到收到整整等了15天。", "label": "讽刺"},
    {"text": "产品本身还行，就是客服态度需要改进。", "label": "中性"},
    {"text": "外观做工都不错，价格也合理，推荐购买！", "label": "正面"},
    {"text": "呵呵，这质量我真是'服'了。", "label": "讽刺"},
    {"text": "用了三天就坏了，心情非常糟糕。", "label": "负面"},
    {"text": "包装挺精美的，其他我不作评价。", "label": "中性"},
    {"text": "售后服务'很有特色'，打三次电话都没人接。", "label": "讽刺"},
    {"text": "物流很快，产品也是我想要的，会回购。", "label": "正面"},
    {"text": "说实话有点失望，和宣传的差距很大。", "label": "负面"},
    {"text": "东西是正品，不过我没怎么用，等用了再来评价。", "label": "中性"},
]

# ======== 三个"坏"Few-shot（故意违反三原则）========
BAD_PROMPTS = {
    "坏1_缺多样性_全正面": """判断情感（正面/负面/中性/讽刺），只输出类别。

评论：太好用了，推荐 → 正面
评论：客服态度棒 → 正面
评论：物流神速好评 → 正面
评论：做工精致喜欢 → 正面

评论：{text}
类别：""",

    "坏2_无边界_全极端": """判断情感（正面/负面/中性/讽刺），只输出类别。

评论：简直完美无敌爱了 → 正面
评论：垃圾废物差评！ → 负面
评论：还行吧 → 中性
评论：呵呵！ → 讽刺

评论：{text}
类别：""",

    "坏3_不代表_教科书例子": """判断情感（正面/负面/中性/讽刺），只输出类别。

评论：好 → 正面
评论：差 → 负面
评论：一般 → 中性
评论：呵 → 讽刺

评论：{text}
类别：""",
}

# 对比：好的 Few-shot（你昨天的版本）
GOOD_PROMPT = """判断评论的情感类别，从「正面/负面/中性/讽刺」中选一个。只输出一个词。

评论：物美价廉，性价比超高
类别：正面

评论：东西有点小问题，但可以接受
类别：中性

评论：这广告吹得天花乱坠，实际品质呵呵
类别：讽刺

评论：收到就坏了，无语
类别：负面

评论：{text}
类别："""

def call(prompt):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=50
    )
    return resp.choices[0].message.content.strip()

def extract_label(output):
    for label in ["讽刺", "正面", "负面", "中性"]:
        if label in output:
            return label
    return "未识别"

def run_one(name, prompt_template):
    correct = 0
    for case in TEST_SET:
        pred = extract_label(call(prompt_template.format(text=case["text"])))
        if pred == case["label"]:
            correct += 1
    return correct

def main():
    print(f"{'Prompt 版本':<30}{'准确率':<15}")
    print("-" * 45)
    print(f"{'✅ 好的 Few-shot':<30}{f'{run_one(None, GOOD_PROMPT)}/10':<15}")
    for name, p in BAD_PROMPTS.items():
        print(f"{'❌ '+name:<30}{f'{run_one(name, p)}/10':<15}")

if __name__ == "__main__":
    main()