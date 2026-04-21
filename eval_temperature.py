import os
from dotenv import load_dotenv
from openai import OpenAI
from collections import Counter

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

PROMPT = "用户评论：'这款耳机音质还行，但戴久了耳朵痛，客服也不理人。' 请提取：1) 正面评价 2) 负面评价 3) 情感极性（正/负/中）。严格用JSON输出，不要多余文字。"

TEMPERATURES = [0, 0.5, 1.0, 1.5]
RUNS = 30

def run():
    print(f"{'温度':<8}{'一致性':<12}{'格式合规率':<14}{'平均长度':<10}")
    print("-" * 50)
    
    for temp in TEMPERATURES:
        outputs = []
        json_ok = 0
        
        for _ in range(RUNS):
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": PROMPT}],
                temperature=temp,
                max_tokens=200
            )
            text = resp.choices[0].message.content.strip()
            outputs.append(text)
            
            # 简单格式检查：是否包含 { 和 }
            if text.startswith("{") and text.endswith("}"):
                json_ok += 1
        
        # 评测指标
        consistency = len(set(outputs)) == 1  # 全部一样?
        unique_ratio = f"{len(set(outputs))}/{RUNS}"
        json_rate = f"{json_ok}/{RUNS}"
        avg_len = sum(len(o) for o in outputs) // RUNS
        
        print(f"{temp:<8}{unique_ratio:<12}{json_rate:<14}{avg_len:<10}")
    
    print("\n💡 你的第一组评测数据已生成。")

if __name__ == "__main__":
    run()