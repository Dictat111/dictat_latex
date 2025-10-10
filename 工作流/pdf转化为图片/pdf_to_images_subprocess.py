import os
import subprocess


def pdf_to_images(pdf_path, density=600, quality=100):
    pdf_dir = os.path.dirname(pdf_path)
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(pdf_dir, f"{pdf_filename}_images")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        command = [
            'convert',
            f'-density', str(density),
            f'-quality', str(quality),
            pdf_path,
            os.path.join(output_folder, f'output.jpg')
        ]
        subprocess.run(command, check=True)
        print(f"图片已成功保存到 {output_folder}")
    except subprocess.CalledProcessError as e:
        print(f"转换过程中出现错误: {e}")
    except FileNotFoundError:
        print("未找到 'convert' 命令，请确保 ImageMagick 已正确安装并配置到系统环境变量中。")


if __name__ == "__main__": #这句话会对地址产生怎么样的影响
    pdf_file_path = "工作流/pdf转化为图片/myth_research.pdf"
    pdf_to_images(pdf_file_path)
    