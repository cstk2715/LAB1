#!/bin/bash
# 这是一个简单的 shell 脚本用来执行当前目录下的 run.py Python 脚本

# 检查 run.py 文件是否存在
if [ -f "run.py" ]; then
    # 如果文件存在，使用 Python 执行
    python run.py "$@"
else
    # 如果文件不存在，输出错误消息
    echo "Error: run.py not found in the current directory."
fi