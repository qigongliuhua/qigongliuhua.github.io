# 1 算法流程

1. 使用Tutte参数化等参数化方法初始化参数网格。
2. 逐三角形计算 $L_t$ 。
3. 根据 $L_t$ ，优化 $E(u,L)=\sum_{t=1}^{T}A_t\|J_t(u)-L_t\|_F^2$ 能量，解得UV坐标
4. 重复2~3。

# 2 具体细节

## 2.1 初始化参数网格

选择使用Floater参数化网格

## 2.2 计算 $L_t$ （局部阶段）

![image-20220801172149474](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208011721537.png)

首先计算每个三角形变换的 Jacobian 矩阵，计算公式如下
$$
J_t(u) = \sum_{i=0}^2 \cot(\theta_t^i)(\mathbf{u}_t^i-\mathbf{u}_t^{i+1})(\mathbf{x}_t^i-\mathbf{x}_t^{i+1})^T \\ 
=
\cot(\theta_t^0)(\mathbf{u}_t^0-\mathbf{u}_t^{1})(\mathbf{x}_t^0-\mathbf{x}_t^{1})^T
+
\cot(\theta_t^1)(\mathbf{u}_t^1-\mathbf{u}_t^{2})(\mathbf{x}_t^1-\mathbf{x}_t^{2})^T
+
\cot(\theta_t^2)(\mathbf{u}_t^2-\mathbf{u}_t^{0})(\mathbf{x}_t^2-\mathbf{x}_t^{0})^T \tag{1}
$$
其中 $\mathbf{u}^i=(u_t^i, v_t^i)^T $ , $\mathbf{x}^i=(x_t^i, y_t^i)^T$ 。

或者
$$
J_t(u) = \begin{bmatrix}
u_t^1-u_t^0 & u_t^2-u_t^0 \\
v_t^1-v_t^0 & v_t^2-v_t^0
\end{bmatrix}
\begin{bmatrix}
x_t^1-x_t^0 & x_t^2-x_t^0 \\
y_t^1-y_t^0 & y_t^2-y_t^0
\end{bmatrix}^{-1} \tag{2}
$$


再对 Jacobian 矩阵进行SVD奇异值分解，得
$$
J_t=U\Sigma V^T=U\begin{bmatrix}
\sigma_1 & 0 \\
0 & \sigma_2
\end{bmatrix}V^T
$$
通过对奇异值 $\sigma_1$ 和 $\sigma_2$ 进行约束，可以得到最优变换矩阵 $L_t$ 

+ 尽可能保角度的参数化扭曲控制方法 ASAP (As-Similar-As-Possible)

$$
L_t = U\begin{bmatrix}
\sigma & 0 \\
0 & \sigma
\end{bmatrix} V^T
$$

其中 $\sigma = (\sigma_1 + \sigma_2)/2$ 。

+ 尽可能保面积方法 AAAP (As-Authalic-As-Possible)

$$
L_t = U\begin{bmatrix}
\sigma & 0 \\
0 & 1/\sigma
\end{bmatrix}V^T
$$

其中 $\sigma$ 是方程 $x^4-\sigma_1 x^3 + \sigma_2 x-1=0$ 的根。

+ 尽可能刚性 ARAP (As-Rigid-As-Possible)

$$
L_t = U\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix}V^T
$$









## 2.3 计算UV坐标（全局阶段）

最小化能量
$$
\begin{aligned}
E(u,L) &= \frac{1}{2}\sum_{t=1}^T\sum_{i=0}^2\cot(\theta_t^i)\Big\| (\mathbf{u}_t^i-\mathbf{u}_t^{i+1})-L_t(\mathbf{x}_t^i-\mathbf{x}_t^{i+1}) \Big\| ^2  \\
&= \frac{1}{2}\sum_{(i,j)\in he}\cot(\theta_{ij})\Big\| (\mathbf{u}_i-\mathbf{u}_j)-L_{t(i,j)}(\mathbf{x}_i-\mathbf{x}_j) \Big\| ^2
\end{aligned}
$$

其中 $he$ 是网格中半边的集合， $u_i$ 和 $x_i$ 是顶点 $i$ 的坐标， $t(i,j)$ 是包含半边 $(i,j)$ 的三角形， $\theta_{ij}$ 是 $t(i,j)$ 中 $(i,j)$ 的对角。令其梯度等于0，可以得到下面这个线性方程组：

$$
\sum_{j\in N(i)}\Big(\cot(\theta_{ij})+\cot(\theta_{ji})\Big)(\mathbf{u}_i-\mathbf{u}_j) 
= \sum_{j\in N(i)}\Big(\cot(\theta_{ij})L_{t(i,j)}+\cot(\theta_{ji})L_{t(j,i)}\Big)(\mathbf{x}_i-\mathbf{x}_j), \tag{3}\\
\forall \, i = 1,\cdots,n.
$$
令
$$
L_{t(i,j)} = \begin{bmatrix}
a_{t_(i,j)} & b_{t_(i,j)} \\
c_{t_(i,j)} & d_{t_(i,j)}
\end{bmatrix} \qquad
\mathbf{u_t} = \begin{bmatrix}
u_t  \\
v_t
\end{bmatrix} \qquad
\mathbf{x_t} = \begin{bmatrix}
x_t  \\
y_t
\end{bmatrix} 
$$
则 (3) 可进一步展开成
$$
\sum_{j\in N(i)}\Big(\cot(\theta_{ij})+\cot(\theta_{ji})\Big)(u_i-u_j)= \\
\sum_{j\in N(i)}\big( \cot(\theta_{ij})a_{t(i,j)} +\cot(\theta_{ji})a_{t(j,i)}\big)(x_i-x_j)
+\big( \cot(\theta_{ij})b_{t(i,j)} +\cot(\theta_{ji})b_{t(j,i)}\big)(y_i-y_j) 
\tag{4} \\ 
\forall \, i = 1,\cdots,n
$$

$$
\sum_{j\in N(i)}\Big(\cot(\theta_{ij})+\cot(\theta_{ji})\Big)(v_i-v_j)= \\
\sum_{j\in N(i)}\big( \cot(\theta_{ij})c_{t(i,j)} +\cot(\theta_{ji})c_{t(j,i)}\big)(x_i-x_j)
+\big( \cot(\theta_{ij})d_{t(i,j)} +\cot(\theta_{ji})d_{t(j,i)}\big)(y_i-y_j)  \tag{5}
\\\forall \, i = 1,\cdots,n
$$

由 (4) 可得 $u_1,u_2,\dots,u_n$ 。由 (5) 可得 $v_1,v_2,\dots,v_n$ 。





























