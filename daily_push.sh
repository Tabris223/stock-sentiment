#!/bin/bash
# 每日舆情推送脚本

cd /Users/damin1206/.openclaw/workspace/stock-sentiment

# 生成日报
REPORT=$(python3 main.py 2>/dev/null)

# 通过 OpenClaw 推送到飞书群
# 群 ID: oc_c9acac4b5dcdf77a2fb8fc2ce8066830

echo "$REPORT"
