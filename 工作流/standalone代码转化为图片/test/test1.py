import sys
sys.path.append("..")
from latex_to_png_converter import LaTeXToPNGConverter


converter = LaTeXToPNGConverter(
    default_border=1,
    default_dpi=600,
    default_quiet=True,
    default_prefix="my_formula",  # 自动命名的默认前缀
    default_output_dir = "output",  # 自动命名的默认输出目录
)

converter.convert(
    latex_content=r"$x^2 + y^2 = r^2$ 圆的方程"
    # 不指定output_filename，将自动生成 my_formula_1.png
)

converter.convert(
    latex_content=r"已知椭圆 $\frac{x^2}{9}+\frac{y^2}{4}=1$ 与直线相交于 $A、B$ 两点, 弦AB的中点为 $M(1, 1)$,求直线 $AB$ 的方程."
    # 不指定output_filename，将自动生成 my_formula_1.png
)

