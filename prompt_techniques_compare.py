import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ======== 测试集（10 条微妙评论 + gold label）========
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

# ======== 4 种 Prompt 技巧 ========

PROMPTS = {
    "zero_shot": lambda text: f"""判断下面这条评论的情感类别，从「正面/负面/中性/讽刺」中选一个。
只输出一个词，不要解释。

评论：{text}
类别：""",

    "few_shot": lambda text: f"""判断评论的情感类别，从「正面/负面/中性/讽刺」中选一个。只输出一个词。

评论：物美价廉，性价比超高
类别：正面

评论：东西有点小问题，但可以接受
类别：中性

评论：这广告吹得天花乱坠，实际品质呵呵
类别：讽刺

评论：收到就坏了，无语
类别：负面

评论：{text}
类别：""",

    "zero_shot_cot": lambda text: f"""判断评论的情感类别，从「正面/负面/中性/讽刺」中选一个。

评论：{text}

让我们一步一步思考：
1) 这句话字面意思是什么？
2) 有没有反语 / 引号 / 夸张的修辞？
3) 作者真实想表达什么？
4) 综合判断类别。

最后一行严格输出：类别：XXX""",

    "few_shot_cot": lambda text: f"""判断评论的情感类别，从「正面/负面/中性/讽刺」中选一个。

评论：这个快递真'神速'，等了10天
思考：注意'神速'加了引号 → 反讽；等10天是负面事实 → 字面是赞，实际是负面 → 讽刺
类别：讽刺

评论：质量不错，但价格偏高
思考：质量评价正面；价格评价负面；整体中性或轻微正面
类别：中性

评论：我家猫超爱这款猫砂！
思考：直白正面评价，无反讽
类别：正面

评论：{text}
思考：
"""
}

def call(prompt):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=300
    )
    return resp.choices[0].message.content.strip()

def extract_label(output):
    """从输出里提取最终类别"""
    for label in ["讽刺", "正面", "负面", "中性"]:
        if label in output.split("\n")[-1]:  # 最后一行优先
            return label
    # 兜底：全文搜索
    for label in ["讽刺", "正面", "负面", "中性"]:
        if label in output:
            return label
    return "未识别"

def run():
    print(f"{'技巧':<20}{'准确率':<15}{'失败case':<40}")
    print("-" * 75)
    
    for tech_name, prompt_fn in PROMPTS.items():
        correct = 0
        failed = []
        for case in TEST_SET:
            output = call(prompt_fn(case["text"]))
            pred = extract_label(output)
            if pred == case["label"]:
                correct += 1
            else:
                failed.append(f"{case['text'][:15]}...({case['label']}→{pred})")
        acc = correct / len(TEST_SET)
        print(f"{tech_name:<20}{f'{correct}/{len(TEST_SET)} ({acc:.0%})':<15}{(failed[0] if failed else 'N/A'):<40}")
    
    print("\n💡 实验完成。观察 4 种技巧的准确率阶梯。")

if __name__ == "__main__":
    run()