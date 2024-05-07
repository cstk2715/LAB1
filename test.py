import subprocess
import time

# 启动local_server.py脚本
local_server_process = subprocess.Popen(["python", "local_server.py"])

# 等待一段时间，确保local_server已经启动完成（可以根据实际情况调整等待时间）
time.sleep(30)

# 启动ChatGLM3.py脚本
subprocess.run(["python", "ChatGLM3.py"])

# 等待local_server.py子进程结束
local_server_process.wait()