import json
import os
import re
class RemoteLLMs:

    def init_local_client(self):
        """
        初始化用户的客户端
        :param args:
        :return:
        """
        raise NotImplementedError()

    def __load_args(self, config_path):
        # 首先读取Config
        self.args = json.load(open(config_path))

    def __init__(self, config_path):
        # 首先读取Config
        self.__load_args(config_path)
        self.max_retries = self.args.get("max_retries", 5)
        self.client = None
        self.filepath = self.args.get("filepath")
        self.language = self.args.get("language")
        self.output = self.args.get("output")
        for idx in range(self.max_retries):
            model = self.init_local_client()
            if model is not None:
                self.client = model
                break
        if self.client is None:
            raise ModuleNotFoundError()

    def create_prompt(self, history, current_query):
        pass

    def request_llm(self, context, seed=1234, sleep_time=1, repeat_times=0):
        pass

    def fit_case(self, pattern: str, data: dict, meta_dict: dict = None):

        if meta_dict is not None:
            for k,v in meta_dict.items():
                pattern = pattern.replace(k, str(v))

        for k, v in data.items():
            pattern = pattern.replace(k, str(v))

        assert '{{' not in pattern, pattern
        assert '}}' not in pattern, pattern
        return pattern


    def interactive_dialogue(self):
        """
        进行交互式的对话，进行模型检查
        :return:
        """
        contexts = []
        while True:
            current_query = input("请输入当前你的对话(输入'CLEAN'清除上下文，'END'离开对话)：")
            if current_query == "CLEAN":
                contexts = []
                print("已经清除上下文")
                continue
            elif current_query == "END":
                return
            contexts = self.create_prompt(current_query, contexts)
            results = self.request_llm(contexts)
            print("%s\t%s" % (results[-1]['role'], results[-1]['content']))

    def POL_Extraction(self):
        try:
            last_position, last_mod_time = self.read_last_position()
            current_mod_time = os.path.getmtime(self.filepath)
            if current_mod_time > last_mod_time:
                print("文件已更新，重新开始处理。")
                last_position = 0  # 重置位置，从头开始
                self.reset_output()  # 重置输出文件
            with open(self.filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            for line_number, line in enumerate(lines, 1):
                if line_number <= last_position:
                    continue  # 跳过已经处理过的行

                # 处理当前行
                prompt = self.create_prompt(line.strip())
                results = self.request_llm(prompt)
                print("%s\t%s" % (results[-1]['role'], results[-1]['content']))

                # 处理返回的 JSON 数据并输出
                self.process_and_save_json(results[-1])

                # 保存当前行号作为新的最后位置
                self.save_last_position(line_number, current_mod_time)

            print(f"抽取完成，已保存至{self.output}")

            # 检查是否到达文件末尾并重置记录
            if line_number == len(lines):
                self.reset_position()

        except FileNotFoundError:
            print("文件未找到，请检查文件路径是否正确")
        except Exception as e:
            print(f"读取文件时发生错误：{str(e)}")

    def create_prompt(self, input_text):
        return f"extract entities from {input_text}"

    def request_llm(self, prompt):
        return [{"role": "test", "content": "test content"}]

    def process_and_save_json(self, result):
        try:
            pattern = r'{.*?}'
            matches = re.findall(pattern, result['content'])
            if matches:
                data = json.loads(matches[-1])
                with open(self.output, 'a', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                    f.write('\n')
            else:
                print("未找到符合的 JSON 数据。")
        except json.JSONDecodeError:
            print("找到的数据不是有效的 JSON 格式。")

    def save_last_position(self, position, mod_time):
        with open('last_position.txt', 'w') as f:
            f.write(f"{position},{mod_time}")

    def read_last_position(self):
        try:
            with open('last_position.txt', 'r') as f:
                position, mod_time = f.read().strip().split(',')
                return int(position), float(mod_time)
        except FileNotFoundError:
            return 0, 0

    def reset_position(self):
        with open('last_position.txt', 'w') as f:
            f.write("0,0")
        # self.reset_output()  # 重置输出文件

    def reset_output(self):
        """
        重置输出文件为初始状态
        """
        with open(self.output, 'w', encoding='utf-8') as f:
            f.write("")  # 清空文件内容
