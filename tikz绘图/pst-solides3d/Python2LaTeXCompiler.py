import subprocess

def convert_pdf_to_png(filename):
    """
    将 PDF 文件转换为 PNG 图片
    :param pdf_filename: PDF 文件路径
    :return: 转换是否成功
    """
    pdf_filename = file_name+".pdf"
    png_filename =  file_name+ ".png"
    try:
        subprocess.run(["convert", "-density", "500", pdf_filename, png_filename], check=True)
        print(f"成功将 {pdf_filename} 转换为 {png_filename}。")
        return True
    except subprocess.CalledProcessError as e:
        print(f"转换过程中出现错误: {e}")
    except FileNotFoundError:
        print("未找到 convert 命令，请确保你已经安装了 ImageMagick。")
    return False
# 定义 LaTeX 文件内容
file_name = "房子状多边形"
code = r"""
%房子形物体
\psset{viewpoint=30 20 20 rtp2xyz, lightsrc=10 5 4,Decran=30}
\begin{pspicture}(-5,-1.8)(4.8,5.4)
    \psSolid[object=new,
    action=draw,
    sommets=
    2 4 3
    -2 4 3
    -2 -4 3
    2 -4 3
    2 4 0
    -2 4 0
    -2 -4 0
    2 -4 0
    0 4 5
    0 -4 5,
    faces={
    [0 1 2 3]
    [7 6 5 4]
    [0 3 7 4]
    [3 9 2]
    [1 8 0]
    [8 9 3 0]
    [9 8 1 2]
    [6 7 3 2]
    [2 1 5 6]}]%
\end{pspicture}
"""

latex_content = """
\\documentclass{{standalone}}
\\usepackage{{pst-solides3d}}   
\\begin{{document}}
{}
\\end{{document}}
""".format(code)

# 定义文件名
tex_filename = f"{file_name}.tex"

# 创建并写入 LaTeX 文件
with open(tex_filename, "w", encoding="utf-8") as file:
    file.write(latex_content)

try:
    # 调用 pdflatex 编译 LaTeX 文件
    subprocess.run(["xelatex", tex_filename], check=True)
    print(f"成功编译 {tex_filename} 为 PDF 文件。")
except subprocess.CalledProcessError as e:
    print(f"编译过程中出现错误: {e}")
except FileNotFoundError:
    print("未找到 pdflatex 命令，请确保你已经安装了 LaTeX 发行版。")

convert_pdf_to_png(file_name)