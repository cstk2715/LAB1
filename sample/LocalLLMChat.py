from transformers import AutoTokenizer, AutoModel

# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained("../model/ZhipuAI/chatglm3-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("../model/ZhipuAI/chatglm3-6b", trust_remote_code=True).quantize(4).cuda()
model = model.eval()

# 初始化对话历史，包含对话模板
history = []

# 定义的消息列表
messages = [
    # {"role": "system", "content": "你是一个专业的抽取命名实体的专家，现在你的工作是“给定一段文本，抽取其中存在的命名实体（人物、地点、机构），分每一个类别存储。"
    #                               "同时你只需要返回以下例子的答案，无需回答其他问题。”"
    #                               "“以下是几个事例”"
    #                               "“例子 1待处理文本:马克·扎克伯格在哈佛大学创立了Facebook，后来公司总部设在加利福尼亚的门洛帕克。"
    #                               "答案:人物{马克·扎克伯格} 地点{哈佛大学, 加利福尼亚, 门洛帕克} 机构{Facebook}”"
    #                               "例子2：Elon Musk, CEO of SpaceX and Tesla, announced the next generation of space travel in Los Angeles"
    #                               "答案：People: {Elon Musk} Places: {Los Angeles} Organizations: {SpaceX, Tesla}"
    #                               "规则:"
    #                               "1.只返回答案"
    #                               "2.答案只有三个元素，人物，地点，机构"
    #                               "3.如果没有答案，返回空集合即可"
    #                               "4.返回的答案请以'答案:人物{} 地点{} 机构{}'的形式返回"
    #                               "明白我的需求以后，请你回复‘我是抽取命名实体专家，孙笑川’"
    #                               },
    {
        "role": "system", "content":
        """
        [Role]
        You are an expert in extracting named entities from text. 
        [SKILL]
    
    
    
        [Task Description]
    
        Your current task is to identify named entities (people, places, organizations) in a given text and categorize them accordingly. 
        You only need to return answers as illustrated in the following examples, and you should not address any other questions."
    
        [EXample]
    
        Example 1:
        Given Text: "Mark Zuckerberg founded Facebook while attending Harvard University, and later the headquarters were established in Menlo Park, California."
        Answer: People: {Mark Zuckerberg} Places: {Harvard University, California, Menlo Park} Organizations: {Facebook}
    
        Example 2:
        Given Text: "Elon Musk, CEO of SpaceX and Tesla, announced the next generation of space travel in Los Angeles."
        Answer: People: {Elon Musk} Places: {Los Angeles} Organizations: {SpaceX, Tesla}
    
        [RULES]
    
        Only return the answer.
        Answers must include three elements: people, places, and organizations.
        If there are no entities, return empty sets.
        Responses should be formatted as 'Answer: People{} Places{} Organizations{}'.
    
        After understanding my requirements, please reply with 'I am an expert in extracting named entities, Sun Xiaochuan'.
        """}
]

# 遍历消息列表，并基于每条消息内容进行对话
for message in messages:
    if message["role"] == "system":
        # 将系统消息作为对话的开头或提示
        prompt = message["content"]
        response, history = model.chat(tokenizer, prompt, history=history)
        print(f"系统提示响应: {response}")

# 进入交互对话循环
while True:
    user_input = input("请输入你的问题（输入'退出'结束对话）：")
    if user_input.lower() == "退出":
        break
    # 基于当前对话历史（包括模板）进行对话
    response, history = model.chat(tokenizer, user_input, history=history)
    print(response)