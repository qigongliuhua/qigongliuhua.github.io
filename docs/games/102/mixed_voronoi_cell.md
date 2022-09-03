> 目的：计算混合voronoi领域的单独一个三角形面积



![image-20220903163426535](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202209031634604.png)



在四边形 $P_1L_1QL_2$ 中，由公共边 $P_1Q$ 可得：
$$
\left\{
\begin{aligned}
\frac{\dfrac{1}{2}L_1}{\cos\theta_2} &=  \frac{\dfrac{1}{2}L_3}{\cos\theta_1} \\
\theta_2 + \theta_1 &= \theta
\end{aligned}
\right.
$$
进一步化简：
$$
\begin{array}{l}
L_1\cos\theta_1 = L_3\cos\theta_2 \\
L_1\cos\theta_1 = L_3\cos(\theta-\theta_1) \\
L_1\cos\theta_1 = L_3(cos\theta\cos\theta_1+\sin\theta\sin\theta_1) \\ 
\cos\theta_1(L_1-L_3\cos\theta) = L_3\sin\theta\sin\theta_1 \\
\cos\theta_1(L_1-L_3\cos\theta) = L_3\sin\theta\sqrt{1-\cos^2\theta_1} \\
\cos^2\theta_1(L_1-L_3\cos\theta)^2 = L_3^2\sin^2\theta(1-\cos^2\theta_1) \\
\end{array}
$$

进一步化简：

$$
\begin{aligned}
\cos^2\theta_1 &= \dfrac{L_3^2\sin^2\theta}{(L_1-L_3\cos\theta)^2 + L_3^2\sin^2\theta} \\
&= \dfrac{L_3^2\sin^2\theta}{L_1^2+L_3^2-2L_1L_3\cos\theta} \\
&= \dfrac{L_3^2\sin^2\theta}{L_2^2} \\
\cos\theta_1 &=\dfrac{L_3}{L_1}\sin\theta
\end{aligned}
$$

则 $\tan\theta_1=\dfrac{\sqrt{L_2^2-L_3^2\sin^2\theta}}{L_3\sin\theta}$ ，同理可得 $\tan\theta_2=\dfrac{\sqrt{L_2^2-L_1^2\sin^2\theta}}{L_1\sin\theta}$ 。又由正弦定理 （ $\dfrac{L_1}{\sin\alpha}=\dfrac{L_2}{\sin\theta}=\dfrac{L_3}{\sin\beta}$ ）可得：
$$
\tan\theta_1=\dfrac{\sqrt{L_2^2-L_2^2\sin^2\beta}}{L_3\sin\theta} = \dfrac{L_2\cos\beta}{L_3\sin\theta} = \cot\beta\\
\tan\theta_2=\dfrac{\sqrt{L_2^2-L_2^2\sin^2\alpha}}{L_1\sin\theta} = \dfrac{L_2\cos\alpha}{L_1\sin\theta} = \cot\alpha
$$
绿色四边形区域面积为：
$$
\begin{aligned}
S &= \dfrac{1}{2}\left(\frac{1}{2}L_1 \right)^2\tan\theta_2 + \dfrac{1}{2}\left(\frac{1}{2}L_3 \right)^2\tan\theta_1 \\
&=\frac{1}{8}(L_1^2\tan\theta_2 + L_3^2\tan\theta_1)\\
&=\frac{1}{8}(L_1^2  \cot\alpha + L_3^2 \cot\beta )\\
\end{aligned}
$$
![image-20220903163426535](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202209031652296.png)



