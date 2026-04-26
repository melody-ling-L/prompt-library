# setup_and_run

## 1) 克隆 GPT-SoVITS

```bash
git clone https://github.com/RVC-Boss/GPT-SoVITS.git
```

假设你当前目录结构如下：

```text
shuziren-release/
GPT-SoVITS/
```

## 2) 创建 Python 3.11 环境

```bash
python3.11 -m venv .venv-gptsovits
source .venv-gptsovits/bin/activate
python -m pip install -U pip setuptools wheel
pip install torch torchvision torchaudio torchcodec
```

## 3) 安装 GPT-SoVITS 依赖

```bash
cd GPT-SoVITS
pip install -r requirements.txt
cd ..
```

## 4) 修正 WebUI 依赖兼容

```bash
bash ./pin_webui_stack.sh
```

## 5) 下载预训练模型

```bash
python ./download_pretrained.py
```

## 6) 启动主页面

```bash
bash ./run_webui.sh
```

- 主页面：`http://127.0.0.1:9874`
- 推理页：在 1C 中开启，通常是 `http://127.0.0.1:9872`

## 7) 浏览器建议

- 优先使用 Safari 进行录音与推理操作。
