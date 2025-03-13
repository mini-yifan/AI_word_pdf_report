import streamlit_mermaid as stmd
import streamlit as st
import time
import re
from gpt_data import *
from md2word import mdtoword, word_to_pdf, process_md_file, set_indent_except_headings
import os
import copy

# 获取当前时间，将当前时间转换为年月日时分秒字符串
def get_current_time():
    current_time = time.localtime()
    year = current_time.tm_year
    month = current_time.tm_mon
    day = current_time.tm_mday
    hour = current_time.tm_hour
    minute = current_time.tm_min
    second = current_time.tm_sec
    time_str = f"{year}-{month:02d}-{day:02d}_{hour:02d}-{minute:02d}-{second:02d}"
    return time_str

st.title("水报告的AI小助手")

col5_1, col5_2, col5_3 = st.columns([6, 8, 2])
with col5_1:
    with open('./site-packages/model_1.txt', 'r', encoding='utf-8') as file:
        model_2 = file.read()

    # 定义主流大语言模型列表
    models2 = ["Pro/deepseek-ai/DeepSeek-V3", "deepseek-ai/DeepSeek-V3", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", "deepseek-ai/DeepSeek-V2.5", "本地模型", "Pro/deepseek-ai/DeepSeek-R1", "deepseek-ai/DeepSeek-R1"]

    # 创建下拉列表，默认选择 DeepSeek
    selected_model2 = st.selectbox(
        "选择一个大语言模型",
        models2,
        index=models2.index(model_2)  # 设置默认选项为 DeepSeek
    )

    with open('./site-packages/model_1.txt', 'w', encoding='utf-8') as file:
        file.write(selected_model2)

with col5_2:
    with open('./site-packages/APIkey.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    API_key = st.text_input("输入API密钥", value=content, type="password")

    with open('./site-packages/APIkey.txt', 'w', encoding='utf-8') as file:
        file.write(API_key)

with col5_3:
    st.markdown("[怎样获得API密钥](https://cloud.siliconflow.cn/account/ak)", )

data = st.file_uploader("上传你的流程图片(支持‘png’, ‘jpg’, ‘jpeg’)：", type=["png", "jpg", "jpeg", "PNG", "JPG", "JPEG"])

if data:
    with st.expander("上传的图片", expanded=True):
        # 显示上传的图片
        st.image(data, caption="上传的图片")

query2 = st.text_area("请输入需求")
text_2 = query2

col2_1, col2_2, col2_3 = st.columns([3, 1, 2])
with col2_1:
    button2 = st.button("生成回答")
with col2_3:
    button3 = st.button("导出Word/pdf文档")
with col2_2:
    # 一个可选框框
    first_line = st.checkbox("首行缩进")

if button2:
    if not query2 and not data:
        st.error("请输入指令或需求")
    elif not API_key:
        st.error("请输入API密钥")
    else:
        with st.spinner("AI思考中，请稍等..."):
            time_tab_3_1 = time.time()
            try:
                if data:
                    response2 = llm_model2(text_2, selected_model2, API_key, data)
                else:
                    response2 = llm_model2(text_2, selected_model2, API_key)

                text_t = llm_text2(response2)
                st.write(text_t)

                # 将respose3存入.md文件
                # 打开（或创建）一个.md文件，并写入Markdown内容
                with open('output.md', 'w', encoding='utf-8') as file:
                    file.write(text_t)
                print("Markdown文件已成功写入.")

            except SyntaxError as e:
                output_e = f"SyntaxError: {e}"
                print("程序出错。", output_e)
                st.error("程序出错。")
            except Exception as e:
                output_e = f"RuntimeError: {e}"
                print("程序出错。", output_e)
                st.error("程序出错。")
            time_tab_3_2 = time.time()
            st.write("请求用时：", time_tab_3_2-time_tab_3_1, "秒")

if button3:
    with st.spinner("正在导出，请稍等..."):
        process_md_file('output.md', 'output.md')
        if os.path.exists('output.md'):
            time_now = get_current_time()

            word_name = "Word文件" + time_now + ".docx"
            mdtoword(word_name)

            if first_line:
                set_indent_except_headings(
                    doc_path=word_name,
                    output_path=word_name,
                    indent_cm=0.74  # 可调整缩进量
                )

            time.sleep(1)

            pdf_name = "PDF文件" + time_now + ".pdf"
            word_to_pdf(word_name, pdf_name)

            # 将output.md文件重命名
            md_name = "文件" + time_now + ".md"
            os.rename('output.md', md_name)

            print("output.md文件已重命名 " + md_name)

            st.success("Word文档已导出到： " + word_name)
            st.success("PDF文档已导出到： " + pdf_name)
            st.success("md文件已保存到： " + md_name)

        else:
            st.error("文件不存在。")


