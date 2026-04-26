# 本地化克隆声音（精简发布包）

这个目录是可发布到 GitHub 的精简版运行包，只保留复现需要的脚本和说明。

## 浏览器要求

- 推荐：**Safari**
- 说明：本地录音在 Safari 下更稳定，Chrome 可能遇到麦克风权限弹窗/超时问题。

## 包含内容

- `run_webui.sh`：启动主 WebUI（9874）
- `pin_webui_stack.sh`：修正 Gradio 依赖兼容（Starlette/FastAPI）
- `download_pretrained.py`：拉取 v2Pro 预训练权重
- `setup_and_run.md`：一步步安装和启动指南

## 不包含内容

- `.venv` 虚拟环境
- 模型权重和缓存
- 日志、临时文件

## 快速使用

按 `setup_and_run.md` 执行即可。
