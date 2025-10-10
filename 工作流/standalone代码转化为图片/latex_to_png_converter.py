import subprocess
import tempfile
import os
from typing import List, Dict, Optional, Union

class LaTeXToPNGConverter:
    """
    增强版LaTeX内容转换为PNG图像的工具类
    
    支持自动命名、批量系列命名、自定义导言区内容，
    提供单文件转换和批量转换功能，支持参数预设和静默模式
    """
    
    def __init__(self, 
                 default_border: int = 10, 
                 default_dpi: int = 300, 
                 default_quiet: bool = False,
                 default_prefix: str = "latex_img",
                 extra_preamble: str = ""):
        """
        初始化转换器
        
        参数:
            default_border: 默认边框大小(pt)，可在转换时覆盖
            default_dpi: 默认分辨率(dpi)，可在转换时覆盖
            default_quiet: 默认是否启用静默模式，可在转换时覆盖
            default_prefix: 自动命名时的默认前缀
            extra_preamble: 附加到LaTeX导言区的内容（如额外宏包）
        """
        # 预设默认参数
        self.default_border = default_border
        self.default_dpi = default_dpi
        self.default_quiet = default_quiet
        self.default_prefix = default_prefix
        self.extra_preamble = extra_preamble  # 额外导言区内容
        
        # 计数器用于自动命名
        self.auto_counter = 1
        
        # LaTeX基础模板
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
        
        # 记录转换历史
        self.conversion_history: List[Dict] = []
    
    def _get_template(self, border: int, content: str) -> str:
        """生成填充后的LaTeX模板，包含额外导言区内容"""
        return self._base_template.replace(
            "{border}", str(border)
        ).replace(
            "{content}", content.strip()
        ).replace(
            "{extra_preamble}", self.extra_preamble.strip()
        )
    
    def _generate_auto_filename(self, prefix: Optional[str]) -> str:
        """生成自动文件名，格式: [前缀]_[序号].png"""
        current_prefix = prefix or self.default_prefix
        filename = f"{current_prefix}_{self.auto_counter}.png"
        
        # 确保文件名不重复
        while os.path.exists(filename):
            self.auto_counter += 1
            filename = f"{current_prefix}_{self.auto_counter}.png"
            
        self.auto_counter += 1
        return filename
    
    def _compile_pdf(self, latex_content: str, border: int, quiet: bool) -> str:
        """编译LaTeX内容为PDF，返回PDF文件路径"""
        # 创建临时目录
        tmpdir = tempfile.mkdtemp()
        tex_path = os.path.join(tmpdir, "document.tex")
        
        # 写入LaTeX文件
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(self._get_template(border, latex_content))
        
        if not quiet:
            print(f"使用临时目录: {tmpdir}")
            print("LaTeX源文件已生成")
        
        # 输出控制
        stdout = subprocess.DEVNULL if quiet else subprocess.PIPE
        
        # 编译PDF（两次确保引用正确）
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
            raise RuntimeError(f"PDF编译失败: {e.stderr}")
        
        # 检查PDF是否生成
        pdf_path = os.path.join(tmpdir, "document.pdf")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError("PDF文件未生成")
            
        if not quiet:
            print(f"PDF文件已生成: {pdf_path}")
            
        return pdf_path
    
    def _convert_pdf_to_png(self, pdf_path: str, output_path: str, dpi: int, quiet: bool) -> None:
        """将PDF转换为PNG图像"""
        if not quiet:
            print(f"开始将PDF转换为PNG（分辨率：{dpi}dpi）...")
        
        try:
            # 转换为PNG
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
            raise RuntimeError(f"PNG转换失败: {e.stderr}")
        
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
        """
        转换单个LaTeX内容为PNG，支持自动命名
        
        参数:
            latex_content: LaTeX内容
            output_filename: 输出PNG文件名，为None则自动命名
            border: 边框大小(pt)，None则使用默认值
            dpi: 分辨率，None则使用默认值
            quiet: 是否静默模式，None则使用默认值
            auto_prefix: 自动命名时的前缀，为None则使用默认前缀
            
        返回:
            转换成功返回True，否则返回False
        """
        # 处理自动命名
        if output_filename is None:
            output_filename = self._generate_auto_filename(auto_prefix)
        
        # 确定参数（使用默认值或传入值）
        current_border = border if border is not None else self.default_border
        current_dpi = dpi if dpi is not None else self.default_dpi
        current_quiet = quiet if quiet is not None else self.default_quiet
        
        try:
            if not current_quiet:
                print("\n" + "="*40)
                print(f"开始转换为: {output_filename}")
                print("="*40)
            
            # 编译PDF
            pdf_path = self._compile_pdf(latex_content, current_border, current_quiet)
            
            # 转换为PNG
            self._convert_pdf_to_png(pdf_path, output_filename, current_dpi, current_quiet)
            
            # 记录成功历史
            self.conversion_history.append({
                "output": output_filename,
                "success": True,
                "error": None
            })
            
            print(f"PNG文件已生成：\n{os.path.abspath(output_filename)}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            # 记录失败历史
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
        """
        批量转换任务，支持系列命名
        
        参数:
            tasks: 任务列表，可以是:
                  - LaTeX内容字符串列表（使用默认参数）
                  - 包含详细参数的字典列表
            series_prefix: 系列命名前缀，为None则使用各任务自身的命名
            start_index: 系列命名的起始序号
            
        返回:
            统计结果字典，包含total, success, failed
        """
        total = len(tasks)
        success = 0
        current_index = start_index
        
        # 标准化任务格式
        normalized_tasks = []
        for task in tasks:
            if isinstance(task, str):
                # 如果是字符串，转换为标准任务字典
                normalized_tasks.append({
                    "latex_content": task,
                    "output_filename": None,
                    "border": None,
                    "dpi": None,
                    "quiet": None
                })
            else:
                # 确保字典包含必要键
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
            # 处理系列命名
            output_filename = task["output_filename"]
            if series_prefix is not None:
                output_filename = f"{series_prefix}_{current_index}.png"
                current_index += 1
            
            print(f"\n处理任务 {i}/{total}: {output_filename or '自动命名'}")
            
            # 检查必要参数
            if not task["latex_content"].strip():
                print("跳过：LaTeX内容为空")
                continue
                
            # 执行转换
            result = self.convert(
                latex_content=task["latex_content"],
                output_filename=output_filename,
                border=task["border"],
                dpi=task["dpi"],
                quiet=task["quiet"]
            )
            
            if result:
                success += 1
        
        # 统计结果
        stats = {
            'total': total,
            'success': success,
            'failed': total - success
        }
        
        print("\n" + "-"*40)
        print(f"批量转换完成：总任务{stats['total']}，成功{stats['success']}，失败{stats['failed']}")
        
        return stats

    def add_to_preamble(self, content: str) -> None:
        """
        向LaTeX导言区添加内容（如额外的宏包或设置）
        
        参数:
            content: 要添加到导言区的LaTeX代码
        """
        if self.extra_preamble:
            self.extra_preamble += "\n" + content
        else:
            self.extra_preamble = content
        print(f"已添加内容到导言区:\n{content}")

# 使用示例
if __name__ == "__main__":
    # 创建转换器实例，设置默认参数
    converter = LaTeXToPNGConverter(
        default_border=1,
        default_dpi=600,
        default_quiet=True,
        default_prefix="my_formula"  # 自动命名的默认前缀
    )
    
    # 向导言区添加额外内容（例如添加tikz宏包用于绘图）
    converter.add_to_preamble(r"""
\usepackage{tikz}
\usetikzlibrary{shapes.geometric}
""")
    
    # 1. 测试自动命名功能（不指定output_filename）
    converter.convert(
        latex_content=r"$x^2 + y^2 = r^2$ 圆的方程"
        # 不指定output_filename，将自动生成 my_formula_1.png
    )
    
    # 2. 测试自定义前缀的自动命名
    converter.convert(
        latex_content=r"$\sin^2\theta + \cos^2\theta = 1$ 三角函数恒等式",
        auto_prefix="trig_identity"  # 自动生成 trig_identity_1.png
    )
    
    # 3. 测试批量转换（使用字符串列表 + 系列命名）
    formulas = [
        r"$E=mc^2$ 质能方程",
        r"$F=ma$ 牛顿第二定律",
        r"$a^2 + b^2 = c^2$ 勾股定理"
    ]
    
    converter.batch_convert(
        tasks=formulas,
        series_prefix="physics_formula",  # 生成 physics_formula_1.png, 2.png...
        start_index=10  # 起始序号从10开始
    )
    
    # 4. 测试批量转换（使用字典列表，混合自定义和自动命名）
    advanced_tasks = [
        {
            "latex_content": r"$\sum_{i=1}^n i = \frac{n(n+1)}{2}$ 求和公式",
            "output_filename": "sum_formula.png",  # 自定义文件名
            "dpi": 800  # 自定义分辨率
        },
        {
            "latex_content": r"$\int_0^1 x^2 dx = \frac{1}{3}$ 定积分示例",
            "border": 5  # 自定义边框
            # 不指定output_filename，使用自动命名
        }
    ]
    
    converter.batch_convert(
        tasks=advanced_tasks
        # 不指定series_prefix，使用各任务自身的命名设置
    )
