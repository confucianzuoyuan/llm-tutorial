数据为：$B \times S \times E$

沿着维度$E$做归一化

$$
\begin{align}
\mu_{b,s} & = \frac{1}{E}\sum_{e=1}^EX_{b,s,e} \\
\text{Var}_{b,s} & = \frac{1}{E}\sum_{e=1}^E(X_{b,s,e}-\mu_{b,s}) \\
\tilde{X}_{b,s,e} & = \frac{X_{b,s,e} - \mu_{b,s}}{\sqrt{ \text{Var}_{b,s} + \epsilon }} \\
Y_{b,s,e} & = \gamma_{e} \cdot \tilde{X}_{b,s,e} + \beta_{e}
\end{align}
$$

从标量函数$L$开始求导，那么有从上游过来的梯度

$$
\frac{\partial\mathcal{L}}{\partial Y_{b,s,e}}
$$

而我们需要求解的导数有

$$
\begin{align}
\frac{\partial \mathcal{L}}{\partial \gamma_{e}} \\
\frac{\partial \mathcal{L}}{\partial \beta_{e}} \\
\frac{\partial \mathcal{L}}{\partial X_{b,s,e}}
\end{align}
$$

