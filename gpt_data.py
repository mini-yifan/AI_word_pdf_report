# -*- coding: utf-8 -*-
from openai import OpenAI
import re
import base64
import streamlit as st
import copy

# 本地模型名称
model_local = "deepseek-r1:1.5b"

def get_image_base64(image_file):
    """Convert an image file to a base64 string."""
    if image_file is not None:
        encoded_string = base64.b64encode(image_file.read()).decode()  # 编码并转换为可读字符串
        return encoded_string
    return None

def llm_model2(content, model=None, API_key=None, image_file=None):
    if model is None:
        model = "deepseek-ai/DeepSeek-V3"
    else:
        model = model

    if model == "本地模型":
        base_url = 'http://localhost:11434/v1/'
        api_key = 'ollama'
        model = model_local
    else:
        #base_url = 'https://api.mindcraft.com.cn/v1/'
        base_url = "https://api.siliconflow.cn/v1/"
        api_key = API_key
    client = OpenAI(base_url=base_url, api_key=api_key)

    if image_file is not None:
        base64_image = get_image_base64(image_file)
        params = {
            "model": "Qwen/Qwen2-VL-72B-Instruct",
            "message": [
                {
                    "role": "system",
                    "content": "你是一个科研报告ai，可以将公式转变为markdown格式输出，根据图片信息将内容写出markdown格式的用“$$”包裹的公式"
                               "输出内容清晰明了，结构严谨"
                               "变量要用标准的markdown格式输出，变量用“$”包裹"
                               "不需要启用markdown代码格式"
                               "不需要启用markdown代码格式"
                               "用中文"
                               "输出不要用'- '分点"


                },
                {
                    "role": "user",
                    "content": [
                        # 使用 base64 编码传输
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low"
                            },
                        },
                        {
                            'type': 'text',
                            'text': '写出公式并详细介绍参数' + content,
                        },
                    ]
                }

            ],
            "temperature": 0,
            "max_tokens": 4000,
            "stream": True
        }

    else:
        params = {
            "model": model,
            "message": [
                {
                    "role": "system",
                    "content": "你是一个科研报告ai，可以将公式转变为markdown格式输出，根据信息将内容写出markdown格式的用“$$”包裹的公式"
                               "输出内容清晰明了，结构严谨"
                               "变量要用标准的markdown格式输出，变量用“$”包裹"
                               "不需要启用markdown代码格式"
                               "不需要启用markdown代码格式"
                               "不要输出短横线'- '"
                               "不要有短横线'- '"

                },
                {
                    "role": "user",
                    "content": content
                }

            ],
            "temperature": 0,
            "max_tokens": 4000,
            "stream": True
        }


    response = client.chat.completions.create(
        model=params.get("model"),
        messages=params.get("message"),
        temperature=params.get("temperature"),
        max_tokens=params.get("max_tokens"),
        stream=params.get("stream"),
    )

    return response


def llm_text2(response):
    text = ''
    for i in response:
        content = i.choices[0].delta.content
        if not content:
            if i.usage:
                print('\n请求花销usage:', i.usage)
                continue
        try:
            st.markdown(content, end='')
        except:
            print(content, end='', flush=True)
        text += content
        #text_to_speech(content)
    else:
        print()
    return text


def AI_run2(content, model, API_key):
    response = llm_model2(content, model, API_key)
    text = llm_text2(response)
    return text


if __name__ == '__main__':
    try:
        while True:
            content = input("写入需求:")
            text = AI_run2(content, model=None, API_key='')
    except KeyboardInterrupt:
        print("程序出错已退出。")