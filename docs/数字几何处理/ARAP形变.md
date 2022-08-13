> **As-Rigid-As-Possible Surface Modeling  **



大体流程同ARAP参数化，只是需要注意的是先全局再局部，初始 $R_i$ 可设为单位矩阵。迭代2~3次即可得到不错的结果。经过测试先局部再全局在cot权的时候效果非常差，不能使用。







# 1. 局部阶段：求 Rt

逐顶点计算：
$$
S_i = \sum_{j \in N(i)} w_{ij} \mathbf{e}_{ij}\mathbf{e_{ij}^{\prime T}}
$$
其中：

+ $w_{ij}$ 是边 $(i,j)$ 的对角余切均值，$w_{ij}=0.5*(\cot\alpha_{ij}+\cot\beta_{ij})$ 。如果是边界边，则只包含一个角；也可以令 $w_{ij}=1$ 。
+ $\mathbf{e_{ij}}$ 是原始网格边 $(i,j)$ 的列向量，$\mathbf{e_{ij}^\prime}$  是形变后的网格边 $(i,j)$ 的列向量，在局部阶段为已知量。



在对 $S_i$ 进行SVD分解得 $S_i=U_i\Sigma_i Vi^T$ 。则 $R_i=V_iU_i^T$ ，如果 $\|R_i\|<0$ ，则让 $U_i$ 的最小奇异值对应的列取反，即第三列取反，以此保证 $\|R_i\|>0$ 。





# 2. 全局阶段：求形变后坐标

根据公式
$$
\sum_{j\in N(i)} w_{ij}(\mathbf{p}_i^\prime-\mathbf{p}_j^\prime)=\sum_{j\in N(i)} 
\frac{w_{ij}}{2}(R_i+R_j)(\mathbf{p}_i-\mathbf{p}_j)
$$
求解 $\mathbf{p}^\prime$ 。对于固定点和移动点则需要对矩阵相应位置单独赋值，来保证求解出来的坐标不变。







![image-20220813134024141](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208131340203.png)

![image-20220813134037892](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208131340933.png)



