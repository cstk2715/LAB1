import argparse
import json
import logging
import ChatGLM3
import local_server
from llms.remote import ChatGPT
import subprocess
import time
def update_config_file(input_file, output_file, args):
    # 读取现有的配置文件
    with open(input_file, 'r', encoding='utf-8') as file:
        config = json.load(file)

    # 更新配置文件参数
    config['model'] = args.model if args.model else config['model']
    config['api_key'] = args.api_key if args.api_key else config['api_key']
    config['base_url'] = args.base_url if args.base_url else config['base_url']
    config['seed'] = args.seed if args.seed is not None else config['seed']
    config['filepath'] = args.filepath if args.filepath else config['filepath']
    config['language'] = args.language if args.language else config['language']
    config['output_path'] = args.output_path if args.output_path else config['output_path']
    # config['quantize'] = args.quantize if args.quantize is not None else config['quantize']

    # 将更新后的配置写回文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)

def main():
    parser = argparse.ArgumentParser(description="更新配置文件参数")
    parser.add_argument('--model', type=str, help='模型名称(chatglm3-6b/gpt-3.5-turbo)',default="chatglm3-6b")
    parser.add_argument('--api_key', type=str, help='API 密钥')
    parser.add_argument('--base_url', type=str, help='基础 URL')
    parser.add_argument('--seed', type=int, help='种子数',default=12345)
    parser.add_argument('--filepath', type=str, help='文件路径(default="txt.txt")',default="txt.txt")
    parser.add_argument('--language', type=str, help='语言(EN/CN)',default="CN")
    parser.add_argument('--output_path', type=str, help='输出文件路径(default="output.txt")',default="output.txt")
    # parser.add_argument('--quantize', type=int, help='量化等级',default=4)
    parser.add_argument('--input_file', type=str,  help='输入配置文件路径(默认为config.json)',default="config.json")
    parser.add_argument('--output_file', type=str,  help='输出配置文件路径(默认为config.json)',default="config.json")

    args = parser.parse_args()

    # 更新配置文件
    try:
        update_config_file(args.input_file, args.output_file, args)
        print("配置文件已更新")
        if args.model == "chatglm3-6b":
            # 启动local_server.py脚本
            local_server_process = subprocess.Popen(["python", "local_server.py"])
            # 等待一段时间，确保local_server已经启动完成（可以根据实际情况调整等待时间）
            time.sleep(30)
            # 启动ChatGLM3.py脚本
            subprocess.run(["python", "ChatGLM3.py"])
            local_server_process.kill()
        else :
            subprocess.run(['python', 'ChatGPT.py'])
            print("remotellm")

    except Exception as e:
        logging.error(f"更新配置文件失败: {str(e)}")
        raise e


if __name__ == '__main__':
    main()

