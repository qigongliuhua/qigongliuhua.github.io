大体思路同ARAP参数化，但是不需要迭代。目前仅能插值平面网格，即原网格和目标网格都是平面网格，因为这样的话得到的Jacobian矩阵可以体现出每个三角面的变换，将这个变换进行插值，然后再根据插值矩阵恢复网格顶点即可得到插值网格。

将Jacobian矩阵SVD分解，表示成旋转矩阵和伸缩矩阵的乘积，如下所示：
$$
A = U\Sigma V^T = (UV^T)(V\Sigma V^T)=R S
$$
根据时间变量 $0\le t \le 1.0$ 进行插值，得到 $A(t)$
$$
A(t) = R(t)((1-t)I+tS)
$$
旋转矩阵 $R(t)$ 可以使用四元数进行插值。

最后再最小化能量 $E=\sum_f \|J-A(t)\|_F^2$ ，可以解得顶点坐标。需要注意一点的是，为了防止插值得到的网格出现”漂移“，可以固定第1个顶点。
$$
\sum_{j\in N(i)}\Big(\cot(\theta_{ij})+\cot(\theta_{ji})\Big)(\mathbf{u}_i-\mathbf{u}_j) \\
= \sum_{j\in N(i)}\Big(\cot(\theta_{ij})L_{t(i,j)}(\mathbf{x}_i^{t(i,j)}-\mathbf{x}_j^{t(i,j)})+\cot(\theta_{ji})L_{t(j,i)}(\mathbf{x}_i^{t(j,i)}-\mathbf{x}_j^{t(j,i)})\Big), \tag{1}\\
\forall \, i = 1,\cdots,n.
$$

![result_1](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208180921283.jpg)

![result_28](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208180921822.jpg)

![result_82](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208180922265.jpg)

![result_120](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208180924481.jpeg)

<video src="../../../../../Projects/iGameMeshView2/iGameMeshView_lite/Model/arap_shape_inter/tttt/video.mp4"></video>

<video src="https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_video/video.mp4"></video>
