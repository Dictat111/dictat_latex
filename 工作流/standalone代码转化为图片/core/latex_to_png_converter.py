import subprocess
import tempfile
import os
import shutil  # 用于复制log和tex文件
from typing import List, Dict, Optional, Union

class LaTeXToPNGConverter:
    """
    增强版LaTeX内容转换为PNG图像的工具类
    
    支持自动命名、批量系列命名、自定义导言区内容，
    提供单文件转换和批量转换功能，支持参数预设和静默模式
    错误时自动保存LaTeX日志和.tex源文件到对应目录
    """
    
    def __init__(self, 
                 default_border: int = 10, 
                 default_dpi: int = 300, 
                 default_quiet: bool = False,
                 default_prefix: str = "latex_img",
                 extra_preamble: str = "",
                 default_output_dir: str = "./",
                 log_dir: str = "./tex_log",  # 日志保存目录
                 tex_dir: str = "./tex_source"  # 新增：失败的.tex文件保存目录
                 ):
        """
        初始化转换器
        
        参数:
            log_dir: LaTeX日志保存目录（默认 ./tex_log）
            tex_dir: 编译失败的.tex源文件保存目录（默认 ./tex_source）
        """
        # 原有参数初始化
        self.default_border = default_border
        self.default_dpi = default_dpi
        self.default_quiet = default_quiet
        self.default_prefix = default_prefix
        self.extra_preamble = extra_preamble
        self.default_output_dir = default_output_dir
        self.auto_counter = 1
        self.conversion_history: List[Dict] = []
        
        # 日志和.tex文件目录初始化
        self.log_dir = log_dir
        self.tex_dir = tex_dir
        self._init_dirs()  # 初始化所有必要目录
        
        # LaTeX基础模板（不变）
        self._base_template = r"""
\documentclass[border={border}pt]{standalone}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{xcolor}
\usepackage{ctex}  % 支持中文显示
{extra_preamble}  % 插入额外的导言区内容
\begin{document}
{content}
\end{document}
        """
    
    def _init_dirs(self) -> None:
        """初始化日志目录和.tex文件目录（不存在则创建）"""
        # 初始化日志目录
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir, exist_ok=True)
            if not self.default_quiet:
                print(f"日志目录已创建：{os.path.abspath(self.log_dir)}")
        
        # 初始化.tex文件保存目录
        if not os.path.exists(self.tex_dir):
            os.makedirs(self.tex_dir, exist_ok=True)
            if not self.default_quiet:
                print(f"LaTeX源文件保存目录已创建：{os.path.abspath(self.tex_dir)}")
    
    def _save_failed_tex_and_logs(self, tmpdir: str, output_filename: str) -> None:
        """
        编译失败时，保存.tex源文件和日志文件到对应目录
        
        参数:
            tmpdir: LaTeX编译的临时目录（含 document.tex 和日志文件）
            output_filename: 当前转换任务的输出文件名（用于文件命名）
        """
        # 提取文件名前缀（不含路径和后缀），确保.tex和日志文件同名关联
        file_prefix = os.path.splitext(os.path.basename(output_filename))[0]
        
        # 1. 保存.tex源文件（核心新增）
        tmp_tex_path = os.path.join(tmpdir, "document.tex")
        target_tex_path = os.path.join(self.tex_dir, f"{file_prefix}.tex")
        if os.path.exists(tmp_tex_path):
            shutil.copy2(tmp_tex_path, target_tex_path)
            if not self.default_quiet:
                print(f"失败的LaTeX源文件已保存：{os.path.abspath(target_tex_path)}")
        
        # 2. 保存日志文件（复用原有逻辑，与.tex文件同名）
        log_file_types = [".log", ".aux", ".out"]
        for file_type in log_file_types:
            tmp_log_path = os.path.join(tmpdir, f"document{file_type}")
            if os.path.exists(tmp_log_path):
                target_log_path = os.path.join(self.log_dir, f"{file_prefix}{file_type}")
                shutil.copy2(tmp_log_path, target_log_path)
                if not self.default_quiet:
                    print(f"日志文件已保存：{os.path.abspath(target_log_path)}")
    
    def _get_template(self, border: int, content: str) -> str:
        """生成填充后的LaTeX模板（不变）"""
        return self._base_template.replace(
            "{border}", str(border)
        ).replace(
            "{content}", content.strip()
        ).replace(
            "{extra_preamble}", self.extra_preamble.strip()
        )
    
    def _generate_auto_filename(self, prefix: Optional[str]) -> str:
        """生成自动命名的文件名（不变）"""
        current_prefix = prefix or self.default_prefix
        filename = f"{current_prefix}_{self.auto_counter}.png"
        full_path = os.path.join(self.default_output_dir, filename)
        dir_path = os.path.dirname(full_path)
        
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except TypeError:
                import pathlib
                pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
            if not self.default_quiet:
                print(f"目标路径不存在，已自动创建：{os.path.abspath(dir_path)}")
        
        while os.path.exists(full_path):
            self.auto_counter += 1
            filename = f"{current_prefix}_{self.auto_counter}.png"
            full_path = os.path.join(self.default_output_dir, filename)
        
        self.auto_counter += 1
        return full_path
    
    def _compile_pdf(self, latex_content: str, border: int, quiet: bool, output_filename: str) -> str:
        """编译LaTeX内容为PDF（修改：调用新的保存方法）"""
        tmpdir = tempfile.mkdtemp()
        tex_path = os.path.join(tmpdir, "document.tex")
        
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(self._get_template(border, latex_content))
        
        if not quiet:
            print(f"使用临时目录: {tmpdir}")
            print("LaTeX源文件已生成")
        
        stdout = subprocess.DEVNULL if quiet else subprocess.PIPE
        
        try:
            if not quiet:
                print("开始第一次编译PDF...")
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
                check=True,
                stdout=stdout,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if not quiet:
                print("开始第二次编译PDF...")
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
                check=True,
                stdout=stdout,
                stderr=subprocess.PIPE,
                text=True
            )
        except subprocess.CalledProcessError as e:
            # 关键修改：调用新方法，同时保存.tex和日志
            self._save_failed_tex_and_logs(tmpdir, output_filename)
            raise RuntimeError(f"PDF编译失败: {e.stderr}") from e
        
        pdf_path = os.path.join(tmpdir, "document.pdf")
        if not os.path.exists(pdf_path):
            # PDF未生成时也保存.tex和日志
            self._save_failed_tex_and_logs(tmpdir, output_filename)
            raise FileNotFoundError("PDF文件未生成")
        
        if not quiet:
            print(f"PDF文件已生成: {pdf_path}")
        
        return pdf_path
    
    def _convert_pdf_to_png(self, pdf_path: str, output_path: str, dpi: int, quiet: bool) -> None:
        """将PDF转换为PNG图像（不变）"""
        if not quiet:
            print(f"开始将PDF转换为PNG（分辨率：{dpi}dpi）...")
        
        try:
            subprocess.run(
                ["convert", 
                 "-density", str(dpi), 
                 "-quality", "100", 
                 "-colorspace", "sRGB", 
                 pdf_path, 
                 output_path],
                check=True,
                stdout=subprocess.DEVNULL if quiet else subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"PNG转换失败: {e.stderr}") from e
        
        if not os.path.exists(output_path):
            raise FileNotFoundError("PNG文件未生成")
        
        if not quiet:
            print(f"PNG文件转换成功")
    
    def convert(self, 
                latex_content: str, 
                output_filename: Optional[str] = None, 
                border: Optional[int] = None, 
                dpi: Optional[int] = None, 
                quiet: Optional[bool] = None,
                auto_prefix: Optional[str] = None) -> bool:
        """转换单个LaTeX内容为PNG（逻辑不变，复用新的保存方法）"""
        if output_filename is None:
            output_filename = self._generate_auto_filename(auto_prefix)
        
        current_border = border if border is not None else self.default_border
        current_dpi = dpi if dpi is not None else self.default_dpi
        current_quiet = quiet if quiet is not None else self.default_quiet
        
        try:
            if not current_quiet:
                print("\n" + "="*40)
                print(f"开始转换为: {output_filename}")
                print("="*40)
            
            pdf_path = self._compile_pdf(latex_content, current_border, current_quiet, output_filename)
            self._convert_pdf_to_png(pdf_path, output_filename, current_dpi, current_quiet)
            
            self.conversion_history.append({
                "output": output_filename,
                "success": True,
                "error": None
            })
            
            print(f"PNG文件已生成：\n{os.path.abspath(output_filename)}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            self.conversion_history.append({
                "output": output_filename,
                "success": False,
                "error": error_msg
            })
            
            print(f"转换失败：{error_msg}")
            return False
    
    def batch_convert(self, 
                     tasks: Union[List[str], List[Dict]], 
                     series_prefix: Optional[str] = None,
                     start_index: int = 1) -> Dict[str, int]:
        """批量转换任务（不变，自动复用失败保存功能）"""
        total = len(tasks)
        success = 0
        current_index = start_index
        
        normalized_tasks = []
        for task in tasks:
            if isinstance(task, str):
                normalized_tasks.append({
                    "latex_content": task,
                    "output_filename": None,
                    "border": None,
                    "dpi": None,
                    "quiet": None
                })
            else:
                normalized_task = {
                    "latex_content": task.get("latex_content", ""),
                    "output_filename": task.get("output_filename"),
                    "border": task.get("border"),
                    "dpi": task.get("dpi"),
                    "quiet": task.get("quiet")
                }
                normalized_tasks.append(normalized_task)
        
        print(f"\n开始批量转换，共{total}个任务")
        print("-"*40)
        
        for i, task in enumerate(normalized_tasks, 1):
            output_filename = task["output_filename"]
            if series_prefix is not None:
                output_filename = f"{series_prefix}_{current_index}.png"
                current_index += 1
            
            print(f"\n处理任务 {i}/{total}: {output_filename or '自动命名'}")
            
            if not task["latex_content"].strip():
                print("跳过：LaTeX内容为空")
                continue
            
            result = self.convert(
                latex_content=task["latex_content"],
                output_filename=output_filename,
                border=task["border"],
                dpi=task["dpi"],
                quiet=task["quiet"]
            )
            
            if result:
                success += 1
        
        stats = {
            'total': total,
            'success': success,
            'failed': total - success
        }
        
        print("\n" + "-"*40)
        print(f"批量转换完成：总任务{stats['total']}，成功{stats['success']}，失败{stats['failed']}")
        
        return stats

    def add_to_preamble(self, content: str) -> None:
        """向LaTeX导言区添加内容（不变）"""
        if self.extra_preamble:
            self.extra_preamble += "\n" + content
        else:
            self.extra_preamble = content
        print(f"已添加内容到导言区:\n{content}")

# 使用示例（测试失败时保存.tex和日志）
if __name__ == "__main__":
    converter = LaTeXToPNGConverter(
        default_border=1,
        default_dpi=600,
        default_quiet=False,  # 显示详细过程
        default_prefix="my_formula",
        log_dir="./tex_log",    # 日志目录
        tex_dir="./tex_source"  # .tex文件保存目录（可自定义）
    )
    
    converter.add_to_preamble(r"""
\usepackage{tikz}
\usetikzlibrary{shapes.geometric}
""")
    
    # 测试：故意写错误LaTeX内容（漏写$），触发.tex和日志保存
    converter.convert(
        latex_content=r"x^2 + y^2 = r^2 圆的方程",  # 错误：缺少$符号
        output_filename="error_test.png"
    )
    
    # 正常转换（不保存.tex和日志）
    converter.convert(
        latex_content=r"$\sin^2\theta + \cos^2\theta = 1$ 三角函数恒等式",
        auto_prefix="trig_identity"
    )
