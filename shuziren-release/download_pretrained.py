#!/usr/bin/env python3
"""Download GPT-SoVITS pretrained weights into GPT-SoVITS/GPT_SoVITS/pretrained_models."""
from __future__ import annotations

import os
import sys

REPO_ID = "lj1995/GPT-SoVITS"
ALLOW_PATTERNS = [
    "s1v3.ckpt",
    "v2Pro/*",
    "sv/*",
    "chinese-hubert-base/**",
    "chinese-roberta-wwm-ext-large/**",
    "models--nvidia--bigvgan_v2_24khz_100band_256x/**",
    "hifigan_config.json",
    "hifigan_do_03357000",
]


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    gpt_root = os.path.join(here, "GPT-SoVITS")
    target = os.path.join(gpt_root, "GPT_SoVITS", "pretrained_models")
    os.makedirs(target, exist_ok=True)

    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("Install first: pip install huggingface_hub", file=sys.stderr)
        return 1

    print(f"Downloading {REPO_ID} -> {target}")
    snapshot_download(
        repo_id=REPO_ID,
        repo_type="model",
        local_dir=target,
        allow_patterns=ALLOW_PATTERNS,
    )
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
