# 实例4：中文标题 + 矩阵行列式转换
import sys
sys.path.append("..")
from core.latex_to_png_converter import LaTeXToPNGConverter
converter = LaTeXToPNGConverter(
    default_border=1,
    default_dpi=600,
    # default_quiet=True,
    default_prefix="多个图片编译的例子",  # 自动命名的默认前缀
    default_output_dir = "多个图片编译的例子",  # 自动命名的默认输出目录

)

# converter.convert(
#     latex_content=r"$x^2 + y^2 = r^2$ 圆的方程"
# )

# converter.convert(
#     latex_content=r"已知椭圆 $\frac{x^2}{9}+\frac{y^2}{4}=1$ 与直线相交于 $A、B$ 两点, 弦AB的中点为 $M(1, 1)$,求直线 $AB$ 的方程."
# )

converter.convert(
    latex_content=r"$$ \frac{x^2}{a^2}+\frac{y^2}{b^2}=1 $$"
)
# converter.convert(
#     latex_content=r"$$\frac{x^2}{b^2}+\frac{y^2}{a^2}=1$$"
# )
# converter.convert(
#     latex_content=r"$$\frac{x^2}{a^2}-\frac{y^2}{b^2}=1$$"
# )
