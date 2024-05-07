import argparse
from openai import OpenAI
from Prompt import CNPROMPT,ENPROMPT

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', choices=['English', 'Chinese'], type=str, help='输入prompt的类型，Chinese,English',
                        default='Chinese')
    args = parser.parse_args()

    # 初始化ChatMindAi客户端
    client = OpenAI(
        api_key="sk-FFklQGpMt6x2BmckfKKTiyCKbPTYLu7xCNaQqRcrhbwtLVH6",
        base_url="https://api.chatanywhere.com.cn/v1"
    )

    # 根据用户选择的语言设置提示
    if args.l == "Chinese":
        prompt = CNPROMPT
    elif args.l == "English":
        prompt = ENPROMPT

    # 初始消息
    messages = [{"role": "system", "content": prompt}]

    # 进行首次请求
    completion = client.chat.completions.create(
        model="ChatMindAi-3.5-turbo-1106",
        messages=messages,
        logprobs=True,
        stream=False
    )
    print(f"系统提示响应: {completion.choices[0].message['content']}")

    # 启动多轮对话循环
    while True:
        user_input = input("请输入你的问题（输入'退出'结束对话）：")
        if user_input.lower() == "退出":
            break

        # 更新消息列表，添加用户和系统的回复
        messages.append({"role": "user", "content": user_input})
        messages.append({"role": "system", "content": prompt})  # 根据需要更新系统提示

        # 请求新的回复
        completion = client.chat.completions.create(
            model="ChatMindAi-3.5-turbo-1106",
            messages=messages,
            logprobs=True,
            stream=False
        )
        # 打印回复并更新历史
        response = completion.choices[0].message['content']
        print(response)
        messages.append({"role": "system", "content": response})


if __name__ == "__main__":
    main()