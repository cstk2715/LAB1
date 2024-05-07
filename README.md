# 实验一
## 任务要求
[实验内容]

1. 设计一个Prompt，完成选题中的一个任务。

2. 需要同时部署本地大模型和使用远程大模型。

3. 需要提供后续的相关应用代码。


[完成人数]
1. 这次作业鼓励单人完成。

2. 本次的部署和之后的作业/期末紧密相关，请认真完成。

3. 单人不限制本地模型的部署类型，3人完成最多和另一个3人的模型一样，6人完成必须独立一种大模型。

4. 无论模型是否和别的组一样，均需要独立完成部署

[选题]

知识挖掘类Prompt：

KE1. 给定一段文本，抽取其中常识知识三元组，每一个三元组的组织形式为（头实体，关系，尾实体）。

KE2. 给定一段文本，抽取其中存在的命名实体（人物、地点、机构等），分每一个类别存储。

KE3. 给定一段文本，以及指定的实体（任五、地点、机构等），抽取与该实体相关的Key-Value知识。


Question-Answer 类Prompt：

QA1. 给定一段背景材料和一个问题和四个答案（A、B、C、D）， 要求模型输出对应的答案以及理由。

QA2. 给定一段背景材料和一个问题， 要求模型写出对应的答案以及理由。

QA3. 给定一段背景材料，要求模型从中发现问题以及答案（即生成问题、答案对）。 

QA4. 给定一段背景材料，以及指定的人物/地点/时间等，要求模型根据给定的信息生成问题和答案。

QA5. 给定一段背景材料，题目，以及正确答案（文字），以及一个学生答案。 设计一个评分Prompt让模型对这个答案进行打分，评分需要是从多个有不同具体含义的指标进行，打分需要在1-10分之间。


[评分要求]

基本要求（每一个⭐️=10分）：

1. [Remote LLM 测试 ⭐️⭐️]      自己准备不少于3个例子，在远程大模型上测试。
2. [Local LLM 测试效果  ⭐️⭐️]   自己准备不少于3个例子（保持同上），在本地大模型上测试。
3. [Local LLM 部署情况 ⭐️]      检查是否已经在本地部署了大模型
4. [Local LLM 应用开发 ⭐⭐️⭐️]    是否已经将所选定的大模型、任务封装成了一个可以直接调用的代码（实现批量输入、批量输出、错误异常管理等，需要自己准备大量测试数据）
5. [文档⭐️⭐️]                  本次作业每个小组都必须以Github/Gitlab项目的方式提交，其中的Readme.md 为本次实验报告的文档。


额外政策：
1. 第二周开始可以检查测试效果和部署效果（前三项），检查周数和分数上限的关系为：第二周-100分，第三周-95分，第四周85分，第五周80分，第六周75分，之后只记60分。
2. 后两项必须在第前三项检查完后再做检查，原则上为检查完两次课内完成（可能会要求返修），之后每延迟一周上限扣减10分，最低上限75。
3. 原则上要获得高分，需要同时提供中文和英文版本的Prompt，给分优先度为： 中文+英文 > 英文 > 中文。
## Linux安装（WSL Ubantu18.04.6 LST）
### 1.途径一  微软商店直接下载
    优点:方便
    缺点:在国内微软商店容易出现连接不稳定的情况
### 2.途径二  在cmd中下载并使用
#### 查看Linux版本
```
wsl --list --online
```
#### 安装你所需要版本的Linux
```
wsl --install -d Ubuntu-18.04 
#此处使用Ubantu-18.04作为示例
```
#### 检查安装是否成功
```
wsl -l
```
#### 若显示你所安装的对应版本即安装成功

## WSL使用，环境配置
### 激活linux环境    
```
wsl -d Ubuntu-18.04
```
### 初次激活
#### 系统将会提示输入用户名以及密码
#### 设置root密码(虽然一般用不到，一般sudo就可以了，root还是比较危险的)
```
sudo passwd root
```
#### 更新系统相关的包
```
sudo apt update
sudo apt upgrade
```
### 

## Python安装与环境配置
### 安装annaconda
#### 选择直接下到wsl对应的linux系统里，或者下好之后移动到wsl的目录里
#### 此处我们选择直接下到linux系统里
```
wget https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
```

#### 安装对应版本的anaconda
```
bash Anaconda3-2024.02-1-Linux-x86_64.sh
```
###### 随后在其中按Q跳过阅读协议，并输入yes(两次)，重启系统
###### (目前conda挺智能的，./bashrc都直接帮你配好)
```
#重启
sudo reboot
```
```
#或者不想重启
source ~/.bashrc
```
#### 创建Python环境
###### conda -n <环境名> python=3.x(你需要的指定版本)
```
conda create -n Python3.10+cuda12.1 python=3.10
```
#### 激活Python环境
```
conda activate Python3.10+cuda12.1
```
#### 安装Pytorch(官网 https://pytorch.org/get-started/locally/)
```
conda install <指定版本>
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```
## Cuda的配置与安装
### 本指南基于 英伟达官网针对wsl2的cuda安装指南 https://docs.nvidia.com/cuda/wsl-user-guide/index.html#getting-started-with-cuda-on-wsl-2
#### PS:如果已经在windows安装了cuda，请不要再次安装，因为两者共享 <br> 同时请误在wsl安英伟达的GPU驱动，一般来说你已经在windows上安装过了</br>
####  
### Cuda Toolkit安装

![img.png](md_image%2Fimg.png)
#### 请到以下链接按以上这样选
```
    https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network
```
#### 有以下三种选择方式，我们选择第二种,按顺序执行下列指令

![img_2.png](md_image%2Fimg_2.png)
```
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-4
```
#### 安装成功与否的验证
```
nvcc -V
```
###### 若显示了对应版本则安装成功
### Cudann的安装
#### 进入官方cudann的下载网站
```    
https://developer.nvidia.com/rdp/cudnn-archive
```
![img_3.png](md_image%2Fimg_3.png)
![img_4.png](md_image%2Fimg_4.png)
#### 选择合适的cudann版本（依照你的cuda版本而定），选择下载Linux x86_64版本
#### 将文件复制到wsl2中，并解压,拷贝文件到cuda中
     tar -xvf <你下载的cudann文件名>
     cd <解压后的文件夹>
     sudo cp ./include/* /usr/local/cuda/include/
     sudo cp ./lib/*  /usr/local/cuda/lib64/
#### 查看是否安装成功
     cat /usr/local/cuda/targets/x86_64-linux/include/cudnn_version.h | grep CUDNN_MAJOR -A 2
![img_5.png](md_image%2Fimg_5.png)
#### 右侧的三个数字应当对应你所下载的版本

## 大语言模型的本地部署
#### 安装相应包(项目根路径下的requirements.txt)
```
cd lab1
conda activate <你的环境>
pip install -r requirements.txt
```
### ChatGLM3

    项目地址:https://github.com/THUDM/ChatGLM3

#### 运行目录下的下载脚本，将模型下载到本地
```
python dowload.py #存储路径为项目根目录下的model文件夹中
```
#### ChatGLM3对话体验(KE2:抽取文本内的人物，机构，地点)
```
cd sample
python LocalLLMChat.py <prompt语言> #English或Chinese 默认Chinese
```
### GPT3
#### 对话体验（KE2:抽取文本内的人物，机构，地点）
```
cd sample 
python RemoteLLMChat.py <prompt语言> #English或Chinese 默认Chinese
```
## 文本KE2抽取脚本使用说明
### 功能说明
#### 本软件实现了通过调用本地大模型/远程大模型实现抽取特定文本中存在的命名实体（人物、地点、机构等），分每一个类别存储。并将抽取结果保存至本地。

### 参数说明
   参数名    |          作用          |               可选项                
:--------:|:--------------------:|:--------------------------------:
 language |  选定prompt的语种(默认中文)   |        CN / EN         
 filepath |     指定待抽取文本文件的路径     |               文件路径               
|  output  |       输出文件的路径        |                    文件路径              |
  model   | 指定使用本地模型或是远程模型(默认本地) |   gpt-3.5-turbo / chatglm3-6b     
| api_key  |     远程模型的apikey      |             api_key              |
| base_url |      远程模型的api网址      | base_url  |

### 文件说明

  文件名    |            作用             
:--------:|:-------------------------:|
 last_position | 存储当前文件以执行到的行数与当前文件最后编辑的时间 |
 output.txt |          默认输出路径           |
 txt.txt |         默认的待处理文本          |
 config.json |          脚本配置文件           |
 sample |    内含远程模型与本地模型的交互体验脚本     |

### 使用说明
跳转至项目根目录,并激活环境
```
cd project
conda activate Python3.10+cuda12.1
```
请提前将待处理文本按行放入你所指定的文件中，随后使用python执行指定脚本
```
python run.py #<可附加的参数>
```
随后文件将输出到output.txt（默认路径）





    
         
    



