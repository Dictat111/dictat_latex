
使用下面的模板出几道对数函数的练习题,标点符号使用半角标点.
```latex
\begin{Exercise}[title={对数运算小练习}, label={ex:logarithm}]
    \Question 计算 $\log_2 8 + \log_3 27$ 的值.
    \Question 已知 $\log_a 2 = m$,$\log_a 3 = n$,求 $\log_a 12$（用 $m$,$n$ 表示）.
    \Question 若 $\log_5 (x + 1) - \log_5 (x - 1) = 1$,求 $x$ 的值.
\end{Exercise}
\begin{MyAnswer}[ref={ex:logarithm}]
        \Question \mybox{答案为 $6$;}\\ 解：根据对数运算法则,$\log_2 8=\log_2 2^3 = 3$,$\log_3 27=\log_3 3^3 = 3$,所以 $\log_2 8+\log_3 27=3 + 3=6$.

        \Question \mybox{答案为 $n + 2m$;}\\ 解：因为 $\log_a 12=\log_a(3\times2^2)$,根据对数运算法则 $\log_a(MN)=\log_a M+\log_a N$ 和 $\log_a M^p = p\log_a M$,可得 $\log_a 12=\log_a 3 + 2\log_a 2$,又已知 $\log_a 2 = m$,$\log_a 3 = n$,所以 $\log_a 12=n + 2m$.

        \Question  \mybox{答案为 $x=\frac{3}{2}$;}\\  解：根据对数运算法则 $\log_a M-\log_a N=\log_a\frac{M}{N}$,则 $\log_5 (x + 1)-\log_5 (x - 1)=\log_5\frac{x + 1}{x - 1}$.已知 $\log_5\frac{x + 1}{x - 1}=1$,即 $\frac{x + 1}{x - 1}=5^1 = 5$.
        方程两边同乘 $x - 1$ 得：$x + 1 = 5(x - 1)$,展开得 $x + 1 = 5x-5$,移项可得 $4x = 6$,解得 $x=\frac{3}{2}$.经检验,当 $x=\frac{3}{2}$ 时,$x + 1=\frac{5}{2}>0$,$x - 1=\frac{1}{2}>0$,满足对数函数的定义域要求.
\end{MyAnswer}

```

为下面这个模板,在原有的基础上,再添加3道题目
```latex
\begin{Exercise}[title={对数运算小练习}, label={ex:logarithm}]
    \Question 计算 $\log_2 8 + \log_3 27$ 的值.
    \Question 已知 $\log_a 2 = m$,$\log_a 3 = n$,求 $\log_a 12$（用 $m$,$n$ 表示）.
    \Question 若 $\log_5 (x + 1) - \log_5 (x - 1) = 1$,求 $x$ 的值.
\end{Exercise}
\begin{MyAnswer}[ref={ex:logarithm}]
        \Question \mybox{答案为 $6$;}\\ 解：根据对数运算法则,$\log_2 8=\log_2 2^3 = 3$,$\log_3 27=\log_3 3^3 = 3$,所以 $\log_2 8+\log_3 27=3 + 3=6$.

        \Question \mybox{答案为 $n + 2m$;}\\ 解：因为 $\log_a 12=\log_a(3\times2^2)$,根据对数运算法则 $\log_a(MN)=\log_a M+\log_a N$ 和 $\log_a M^p = p\log_a M$,可得 $\log_a 12=\log_a 3 + 2\log_a 2$,又已知 $\log_a 2 = m$,$\log_a 3 = n$,所以 $\log_a 12=n + 2m$.

        \Question  \mybox{答案为 $x=\frac{3}{2}$;}\\  解：根据对数运算法则 $\log_a M-\log_a N=\log_a\frac{M}{N}$,则 $\log_5 (x + 1)-\log_5 (x - 1)=\log_5\frac{x + 1}{x - 1}$.已知 $\log_5\frac{x + 1}{x - 1}=1$,即 $\frac{x + 1}{x - 1}=5^1 = 5$.
        方程两边同乘 $x - 1$ 得：$x + 1 = 5(x - 1)$,展开得 $x + 1 = 5x-5$,移项可得 $4x = 6$,解得 $x=\frac{3}{2}$.经检验,当 $x=\frac{3}{2}$ 时,$x + 1=\frac{5}{2}>0$,$x - 1=\frac{1}{2}>0$,满足对数函数的定义域要求.
\end{MyAnswer}

```