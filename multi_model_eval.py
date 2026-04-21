import os
import time
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ======== 模型配置（可插拔）========
MODELS = [
    {
        "name": "DeepSeek V3",
        "model_id": "deepseek-chat",
        "base_url": "https://api.deepseek.com",
        "api_key_env": "DEEPSEEK_API_KEY",
    },
    {
        "name": "DeepSeek R1",
        "model_id": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com",
        "api_key_env": "DEEPSEEK_API_KEY",
    },
    # 有 Qwen 时再加：
    {
        "name": "Qwen2.5-Max",
        "model_id": "qwen-max",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key_env": "DASHSCOPE_API_KEY",
    },
]

# ======== 测试集（5 个 B 端典型任务）========
TEST_CASES = [
    {
        "id": "extract_json",
        "prompt": "用户评论：'这款耳机音质还行，但戴久了耳朵痛，客服也不理人。' 提取：1)正面 2)负面 3)情感极性。严格JSON输出。",
        "expected_keys": ["正面", "负面", "情感极性"],
    },
    {
        "id": "reasoning",
        "prompt": "一个水池有两个水管，A管单独灌满需要3小时，B管单独灌满需要6小时。两管同时开，多久灌满？请一步步思考。",
        "expected_contains": ["2"],
    },
    {
        "id": "code_gen",
        "prompt": "用 Python 写一个函数 is_prime(n)，判断 n 是否质数。只给代码，不要解释。",
        "expected_contains": ["def is_prime"],
    },
    {
        "id": "chinese_rewrite",
        "prompt": "把下面文案改写成更活泼的小红书风格，不超过50字：'我们的新款耳机音质出色，降噪效果好，适合长时间佩戴。'",
        "expected_contains": [],  # 主观任务，人工看
    },
    {
        "id": "instruction_follow",
        "prompt": "列出3个适合程序员的爱好，每个用一句话描述。格式严格为：1.XXX：YYY 2.XXX：YYY 3.XXX：YYY",
        "expected_contains": ["1.", "2.", "3."],
    },
]

def call_model(cfg, prompt):
    client = OpenAI(api_key=os.getenv(cfg["api_key_env"]), base_url=cfg["base_url"])
    # 推理模型需要更多 token
    max_tok = 4000 if "reason" in cfg["model_id"].lower() or "r1" in cfg["name"].lower() else 500
    start = time.time()
    resp = client.chat.completions.create(
        model=cfg["model_id"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=max_tok
    )
    elapsed = time.time() - start
    return {
        "output": resp.choices[0].message.content.strip(),
        "prompt_tokens": resp.usage.prompt_tokens,
        "completion_tokens": resp.usage.completion_tokens,
        "latency_sec": round(elapsed, 2)
    }
    

import re

def _extract_json(text):
    """从可能包含 markdown 代码块的文本中提取 JSON"""
    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 尝试匹配 ```json ... ``` 或 ``` ... ```
    match = re.search(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    # 尝试找第一个 { 到最后一个 }
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None

def evaluate(case, output):
    score = {"pass": True, "reasons": []}
    if "expected_keys" in case:
        parsed = _extract_json(output)
        if parsed is None:
            score["pass"] = False
            score["reasons"].append("JSON 解析失败（已尝试 markdown 包裹）")
        else:
            for k in case["expected_keys"]:
                if k not in parsed:
                    score["pass"] = False
                    score["reasons"].append(f"缺字段 {k}")
    for kw in case.get("expected_contains", []):
        if kw not in output:
            score["pass"] = False
            score["reasons"].append(f"缺关键词 {kw}")
    return score

def main():
    all_results = {}
    for cfg in MODELS:
        print(f"\n{'='*60}")
        print(f"🤖 测试模型：{cfg['name']}")
        print('='*60)
        model_results = []
        for case in TEST_CASES:
            print(f"\n  📝 任务: {case['id']}")
            try:
                r = call_model(cfg, case["prompt"])
                eval_r = evaluate(case, r["output"])
                print(f"    输出: {r['output'][:80]}...")
                print(f"    延迟: {r['latency_sec']}s | tokens: {r['prompt_tokens']}/{r['completion_tokens']}")
                print(f"    通过: {'✅' if eval_r['pass'] else '❌ ' + ', '.join(eval_r['reasons'])}")
                model_results.append({**r, "case_id": case["id"], **eval_r})
            except Exception as e:
                print(f"    ⚠️ 报错: {e}")
                model_results.append({"case_id": case["id"], "pass": False, "reasons": [str(e)]})
        all_results[cfg["name"]] = model_results
    
    # 汇总
    print(f"\n{'='*60}")
    print("📊 汇总")
    print('='*60)
    print(f"{'模型':<20}{'通过率':<12}{'平均延迟':<12}{'总输出tokens':<15}")
    for name, results in all_results.items():
        passed = sum(1 for r in results if r.get("pass"))
        avg_latency = sum(r.get("latency_sec", 0) for r in results) / len(results)
        total_out = sum(r.get("completion_tokens", 0) for r in results)
        print(f"{name:<20}{f'{passed}/{len(results)}':<12}{f'{avg_latency:.2f}s':<12}{total_out:<15}")

if __name__ == "__main__":
    main()