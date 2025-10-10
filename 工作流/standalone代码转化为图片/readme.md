# LaTeXToPNGConverter

## 使用方法
### 创建转换器实例，设置默认参数
```python
converter = LaTeXToPNGConverter(
    default_border=1,
    default_dpi=600,
    default_quiet=True,
    default_prefix="my_formula"  # 自动命名的默认前缀
)
```
### 向导言区添加额外内容（例如添加tikz宏包用于绘图）
```python
converter.add_to_preamble(r"""
\usepackage{tikz}
\usetikzlibrary{shapes.geometric}
""")
```
### 测试自动命名功能（不指定output_filename）
```python

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
```