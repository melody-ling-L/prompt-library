import os
from dotenv import load_dotenv
from openai import OpenAI
from collections import defaultdict

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

PROMPT = "写一句中文广告语，推广一款面向程序员的人体工学椅。要求简短有力，不超过20字。"
TEMPERATURES = [0, 1.0, 1.5]
RUNS_PER_TEMP = 3

def run_experiment():
    results = defaultdict(list)
    
    for temp in TEMPERATURES:
        print(f"\n{'='*60}")
        print(f"🌡  temperature = {temp}")
        print('='*60)
        
        for i in range(RUNS_PER_TEMP):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": PROMPT}],
                temperature=temp,
                max_tokens=100
            )
            output = response.choices[0].message.content.strip()
            results[temp].append(output)
            print(f"  [{i+1}] {output}")
    
    # 分析
    print(f"\n{'='*60}")
    print("📊 分析")
    print('='*60)
    for temp in TEMPERATURES:
        outputs = results[temp]
        unique_count = len(set(outputs))
        print(f"temperature={temp}: {unique_count}/{RUNS_PER_TEMP} 个不同输出")

if __name__ == "__main__":
    run_experiment()