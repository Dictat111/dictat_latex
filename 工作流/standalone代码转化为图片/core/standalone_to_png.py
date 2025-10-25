import subprocess
import tempfile
import os

def latex_to_png(latex_content, output_filename="output.png", border=10, dpi=300, quiet=False):
    """
    将LaTeX内容先转换为PDF，再转换为PNG图像
    
    参数:
        latex_content: 要转换的LaTeX内容（不包含文档类和环境）
        output_filename: 输出的PNG文件名
        border: 图像边框大小（pt）
        dpi: 图像分辨率（dots per inch），值越高越清晰
        quiet: 是否启用静默模式（跳过编译过程的详细输出）
               设为True时仅显示关键进度信息，错误时仍会显示错误详情
    """
    # 定义standalone模板
    template = r"""
\documentclass[border={border}pt]{standalone}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{xcolor}
\usepackage{ctex}  % 支持中文显示
\begin{document}
{content}
\end{document}
    """
    
    # 替换模板中的占位符
    template = template.replace("{border}", str(border))
    template = template.replace("{content}", latex_content.strip())
    if not quiet:
        print("模板生成完成")

    # 创建临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        if not quiet:
            print(f"使用临时目录: {tmpdir}")
        
        # 写入LaTeX文件
        tex_file = os.path.join(tmpdir, "document.tex")
        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(template.strip())
        if not quiet:
            print("LaTeX源文件已生成")

        try:
            # 输出控制：静默模式下重定向输出到DEVNULL
            output_target = subprocess.DEVNULL if quiet else subprocess.PIPE
            
            # 第一步：使用xelatex生成PDF，添加非交互模式避免卡住
            if not quiet:
                print(f"开始第一次编译PDF（DPI设置：{dpi}）...")
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_file],
                check=True,
                stdout=output_target,
                stderr=subprocess.PIPE,  # 错误信息始终捕获
                text=True
            )
            
            # 第二次编译确保引用正确
            if not quiet:
                print("开始第二次编译PDF...")
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_file],
                check=True,
                stdout=output_target,
                stderr=subprocess.PIPE,  # 错误信息始终捕获
                text=True
            )
            
            # 检查PDF文件是否生成
            pdf_file = os.path.join(tmpdir, "document.pdf")
            if not os.path.exists(pdf_file):
                raise FileNotFoundError("PDF文件生成失败")
            if not quiet:
                print(f"PDF文件已生成: {pdf_file}")
            
            # 第二步：使用convert命令将PDF转换为PNG
            png_temp_file = os.path.join(tmpdir, "document.png")
            if not quiet:
                print(f"开始将PDF转换为PNG（分辨率：{dpi}dpi）...")
            
            # 使用convert命令，指定密度确保清晰度
            subprocess.run(
                ["convert", 
                 "-density", str(dpi),  # 控制分辨率
                 "-quality", "100",     # 最高质量
                 "-colorspace", "sRGB", # 确保颜色正确
                 pdf_file, 
                 png_temp_file],
                check=True,
                stdout=output_target,
                stderr=subprocess.PIPE,  # 错误信息始终捕获
                text=True
            )
            
            # 读取生成的PNG文件
            if not os.path.exists(png_temp_file):
                raise FileNotFoundError("PNG文件转换失败")
            if not quiet:
                print(f"PNG临时文件生成成功")
            
            # 保存到输出文件
            with open(png_temp_file, "rb") as f:
                png_content = f.read()
            
            with open(output_filename, "wb") as f:
                f.write(png_content)
            
            # 无论是否静默模式，都显示最终结果
            print(f"PNG文件已生成：\n{os.path.abspath(output_filename)}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"命令执行错误：{e.stderr}")
            return False
        except Exception as e:
            print(f"发生错误：{str(e)}")
            return False

if __name__ == "__main__":
    # 测试用的LaTeX内容（包含公式和中文）
    latex_code = r"""
$x^2=1$ 为什么会这样子呢
    """
    
    # 转换为PNG，设置quiet=True跳过编译过程的输出
    latex_to_png(
        latex_content=latex_code,
        output_filename="result.png",
        border=1,
        dpi=2000,
        quiet=True  # 设为True启用静默模式，False显示详细过程
    )
