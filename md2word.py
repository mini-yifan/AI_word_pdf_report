import pypandoc

import pythoncom
from docx2pdf import convert

from docx import Document
from docx.shared import Cm  # 支持厘米单位[6]()


def word_to_pdf(input_word_path, output_pdf_path):
    """
    将Word文档转换为PDF
    :param input_word_path: 输入Word文件的路径（例如：'input.docx' ）
    :param output_pdf_path: 输出PDF文件的路径（例如：'output.pdf' ）
    """
    try:
        # 初始化COM接口
        pythoncom.CoInitialize()
        # 调用docx2pdf的convert函数进行转换
        convert(input_word_path, output_pdf_path)
        print(f"转换成功！PDF文件已保存为：{output_pdf_path}")
    except Exception as e:
        print(f"转换失败：{e}")
    finally:
        # 释放COM接口
        pythoncom.CoUninitialize()

# 将markdown文件转换为word文件
def mdtoword(outputfile='output.docx'):
    # 转换配置参数
    extra_args = [
        "--listings",           # 强制识别列表结构
        "--toc-depth=6",        # 允许深层列表
        "--extract-media=./",   # 处理公式中的图片
    ]

    # convert all markdown files in a chapters/ subdirectory.
    pypandoc.convert_file('output.md', 'docx', format='markdown', outputfile=outputfile, extra_args=extra_args)
    print("Markdown文件已成功写入.")

# 将markdown文件转换为html文件
def mdtohtml(outputfile='output.html'):
    # convert all markdown files in a chapters/ subdirectory.
    pypandoc.convert_file('output.md', 'html', outputfile=outputfile)
    print("Markdown文件已成功写入.")


def process_md_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = []
    for line in lines:
        if line.startswith('- '):
            # 去除"- "前缀并去除左侧多余空格
            content = line[len('- '):].lstrip()
            # 重新构建为规范化的列表项
            processed_line = f' {content}'
            print(processed_line)
        else:
            processed_line = line
        processed_lines.append(processed_line)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)

def set_indent_except_headings(doc_path, output_path, indent_cm=0.74):
    """设置非标题段落的首行缩进

    Args:
        doc_path (str): 输入文档路径
        output_path (str): 输出文档路径
        indent_cm (float): 缩进距离（厘米），默认0.74cm≈2个五号字符[8]()
    """
    doc = Document(doc_path)

    for paragraph in doc.paragraphs:
        # 排除标题段落（包括所有级别的标题）
        if not paragraph.style.name.startswith('Heading'):
            # 设置首行缩进
            paragraph_format = paragraph.paragraph_format
            paragraph_format.first_line_indent = Cm(indent_cm)  # 使用厘米单位[6]()

    doc.save(output_path)


if __name__ == '__main__':
    #mdtoword()
    #process_md_file('文件2025-03-12_10-44-07.md', 'e.md')
    # 使用示例
    set_indent_except_headings(
        doc_path="Word文件2025-03-12_10-57-39.docx",
        output_path="e.docx",
        indent_cm=0.74  # 可调整缩进量
    )

