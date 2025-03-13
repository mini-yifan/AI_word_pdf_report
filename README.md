# AI_word_pdf_report
这是一个可以自动将AI写的报告内容导出word和pdf的软件，导出后文件排版和公式格式不变。

本项目调用大语言模型的API接口，用python代码实现将AI输出内容转换格式导入到word和pdf中

项目用streamlit编写界面

文件**main.py**：streamlit界面代码

文件**gpt_api.py**：调用API接口

文件**md2word.py**：转换文件格式的函数

文件**requirements.txt**：所需要的python依赖库

运行命令 `pip install -r requirements.txt` 即可安装所有所需依赖。

运行命令 `streamlit run main.py` 即可运行网站程序
