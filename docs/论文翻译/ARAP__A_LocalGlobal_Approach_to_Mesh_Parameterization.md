> **A Local/Global Approach to Mesh Parameterization**



# 摘要

$\quad$ We present a novel approach to parameterize a mesh with disk topology to the plane in a shape-preserving manner. Our key contribution is a local/global algorithm, which combines a local mapping of each 3D triangle to the plane, using transformations taken from a restricted set, with a global "stitch" operation of all triangles, involving a sparse linear system. The local transformations can be taken from a variety of families, e.g. similarities or rotations, generating different types of parameterizations. In the first case, the parameterization tries to force each 2D triangle to be an as-similar-as-possible version of its 3D counterpart. This is shown to yield results identical to those of the LSCM algorithm. In the second case, the parameterization tries to force each 2D triangle to be an as-rigid-as-possible version of its 3D counterpart. This approach preserves shape as much as possible. It is simple, effective, and fast, due to pre-factoring of the linear system involved in the global phase. Experimental results show that our approach provides almost isometric parameterizations and obtains more shape-preserving results than other state-of-the-art approaches. 

$\quad$ 我们提出了一种新方法，以保形方式将具有圆盘拓扑的网格参数化到平面。我们的主要贡献是一种局部/全局算法，该算法使用从受限集获取的变换，将每个 $3D$ 三角形的局部映射结合到平面，并对所有三角形进行全局“缝合”操作，涉及稀疏线性系统。局部变换可以来自各种族，例如相似性或旋转，生成不同类型的参数化。在第一种情况下，参数化试图强制每个 $2D $三角形成为其 $3D$ 对应物的尽可能相似的版本。结果表明，这可以得到与 $LSCM$ 算法相同的结果。在第二种情况下，参数化试图强制每个二维三角形成为其三维对应物的尽可能保刚性的版本。这种方法尽可能地保持形状。由于全局阶段中涉及的线性系统的预分解，该方法简单、有效、快速。实验结果表明，与其他最先进的方法相比，我们的方法提供了几乎等距的参数化，并获得了更多的保形结果。

$\quad$ We present also a more general "hybrid" parameterization model which provides a continuous spectrum of possibilities, controlled by a single parameter. The two cases described above lie at the two ends of the spectrum. We generalize our local/global algorithm to compute these parameterizations. The local phase may also be accelerated by parallelizing the independent computations per triangle.

$\quad$ 我们还提出了一个更通用的“混合”参数化模型，该模型提供了由单个参数控制的连续可能性谱。上述两种情况位于光谱的两端。我们推广了局部/全局算法来计算这些参数化。也可以通过并行每个三角形的独立计算来加速局部阶段。

# 1 引言

$\quad$ Surface parameterization of 3D models is an important component in various computer graphics and geometry processing applications, such as filtering, compression, recognition, texture mapping, and morphing. It involves computing a bijective mapping between a piecewise-linear triangulated surface and a suitable parameter domain. In this paper we consider the parameterization of a surface having the topology of the disk, possibly with boundaries, onto the plane.

$\quad$ 三维模型的表面参数化是各种计算机图形学和几何处理应用中的一个重要组成部分，例如过滤、压缩、识别、纹理映射和变形。它涉及计算分段线性三角化曲面和适当参数域之间的双射映射。**在本文中，我们考虑在平面上具有圆盘拓扑（可能具有边界）的曲面的参数化。** 

$\quad$ In general, the parameterization will incur some metric distortion, since only developable surfaces can be flattened onto the plane without any distortion. Hence, the goal of parameterization is to find a bijective mapping which preserves some geometric properties of the original as much as possible, e.g., authalic (area-preserving) mapping, conformal (angle-preserving) mapping, isometric (length-preserving) or some combination of these. Each individual triangle may be easily parameterized without distortion, but then they will no longer fit together properly in the plane.

$\quad$ 一般来说，参数化会产生一些度量失真，因为只有可展曲面可以在没有任何失真的情况下展平到平面上。因此，参数化的目标是找到一个双射映射，该映射尽可能保留原始的一些几何特性，例如等面积（保持面积）映射、保角（保持角度）映射、等距（保持长度）或这些的一些组合。每个单独的三角形可以很容易地参数化且不失真，但它们在平面中却不能很好地匹配彼此。

$\quad$ Inspired by recent work on mesh deformation and modeling [IMH05, SA07], we formulate the parameterization problem as an optimization problem having both local and global elements. In essence, we seek for local transformations which minimize the distortion of each mesh triangle, yet require that they all fit together to a coherent 2D triangulation. We follow closely the method for "as-rigidas-possible" deformation of triangle meshes described by Sorkine and Alexa [SA07] for mesh editing purposes, and, essentially, apply the same methodology to the problem of mesh parameterization.

$\quad$ 受最近关于网格变形和建模的工作的启发 `[IMH05, SA07]` ，我们将参数化问题表述为具有局部和全局元素的优化问题。本质上，我们寻求局部变换，以最小化每个网格三角形的失真，但要求他们都匹配彼此以形成一个连贯的2D三角剖分。为了编辑网格，我们遵循 $Sorkine$ 和 $Alexa$  `[SA07]` 所描述的三角形网格的“尽可能刚性”变形方法，本质上，将相同的方法应用于网格参数化问题。

# 2 先前的工作

$\quad$ In the past decade, methods for triangular mesh parameterization have been studied extensively. We refer the interested reader to [FH05] and [SPR06] for a survey of the state-ofthe-art in parameterization research.

$\quad$ 近十年来，三角网格参数化方法得到了广泛的研究。我们推荐有兴趣的读者参考 `[FH05]` 和 `[SPR06]` ，以了解参数化研究的最新进展。

$\quad$ The linear setting for parameterization offers the advantage of simplicity and validity of parameterization results. Based on Tutte’s barycentric mapping theorem [Tut63], Eck et al. [EDD*95] and Floater [Flo97] described a simple approach to parameterization by representing each interior vertex as some convex combination of its neighboring vertices. Depending on the precise weights used, it is possible to achieve a variety of effects, minimizing various distortion measures. The most celebrated weight recipes are the so-called cotangent weights [PP93], and the so-called mean-value weights [Flo03], which are both related to harmonic mappings. Unfortunately, the method of barycentric coordinates requires the boundary of the mesh to be fixed to a convex polygon in the plane, which is somewhat arbitrary, typically resulting in significant distortion. Lee et al. [LKL02] alleviated this somewhat by "padding" the mesh with a virtual boundary, allowing the true boundary to evolve to a less distorted shape. Desbrun et al. [DMA02] were able to generalize the method of barycentric coordinates so that also the boundary vertices are free, subject to socalled "natural" boundary conditions - some additional linear equations. This was shown to be equivalent to the LeastSquares Conformal Mapping (LSCM) method of Levy et al. [LPRM02], which is a least-squares approximation of the discrete Cauchy-Riemann equations, which define continuous conformal mappings. These boundary equations were generalized by Karni et al. [KGG05] to a larger family of barycentric coordinates.

$\quad$ 参数化线性设置具有参数化结果简单、有效的优点。基于 $Tutte$ 的重心映射定理 `[Tut63]` ， $Eck$ 等人`[EDD*95]` 和 $Floater$ `[Flo97]` 描述了一种简单的参数化方法，将每个内部顶点表示为其相邻顶点的某种凸组合。根据所使用的精确权重，有可能实现多种效果，最大限度地减少各种失真措施。最著名的权重公式是所谓的余切权重 `[PP93]` 和所谓的均值权重 `[Flo03]` ，它们都与调和映射有关。遗憾的是，重心坐标法要求网格的边界固定在平面上的凸多边形上，这有点武断，通常会导致严重的失真。$Lee$ 等人 `[LKL02]` 通过用虚拟边界“填充”网格来缓解这一问题，允许实际的边界演变成不那么扭曲的形状。$Desbrun$ 等人 `[DMA02]` 能够推广重心坐标的方法，以便边界顶点也是自由的，受制于所谓的“自然”边界条件——一些额外的线性方程。这被证明等价于 $Levy$ 等人 `[LPRM02]` 的最小二乘共形映射（ **LSCM** ）方法，该方法是离散柯西-黎曼方程的最小二乘逼近，它定义了连续的共形映射。$Karni$ 等人 `[KGG05]` 将这些边界方程推广到更大的重心坐标族。

$\quad$ The main problem with linear free-boundary methods is that the parameterization is no longer guaranteed to be bijective, meaning that the resulting 2D embedding may contain local overlaps (also known as "triangle flips"), global overlaps, or even wind on itself. Karni et al. [KGG05] showed how to solve the more frequent problem of local overlaps in a postprocessing step.

$\quad$ 线性自由边界方法的主要问题是参数化不再保证是双射的，这意味着最终的2D嵌入可能包含局部重叠（也称为“三角翻转”），全局重叠，甚至缠绕自身。 $Karni$ 等人 `[KGG05]` 展示了如何在后处理步骤中解决更频繁的局部重叠问题。

$\quad$ Some parameterization work focuses on directly optimizing the distortion metrics of length, angle or area. These approaches require extensive computation, since the distortion measures are usually highly non-linear. Hormann et al. [HG99] define a deformation-based MIPS energy which requires a non-linear solver. The compute-intensive ABF method of Sheffer et al. [SdS00] computes the parameterization in angle space, with a result minimizing angular distortion. The more efficient ABF++ [SLMB05] and LinABF [ZLS07] have accelerated this method considerably. Other metrics are also used to guide the optimization process for parameterization, such as stretch. These are based on the singular values of the Jacobian matrix of the parameterization mapping [SSGH01], on the Green-Lagrange tensor [MYV93, ZMT05] or the synthesized distortion metric [YYS06].

$\quad$ 一些参数化工作侧重于直接优化长度、角度或面积的失真度量。这些方法需要大量的计算，因为失真测量通常是高度非线性的。 $Hormann$ 等人 `[HG99]` 定义了一种基于变形的 **MIPS** 能量，该能量需要非线性求解器。 $Sheffer$ 等人 `[SdS00]` 的计算密集型 **ABF** 方法在角度空间中计算参数化，其结果是最小的角畸变。更高效的 **ABF++** `[SLMB05]`和 **LinABF**  `[ZLS07]` 大大加快了该方法的速度。其他指标也用于指导参数化的优化过程，如拉伸。这些是基于参数化映射 `[SSGH01]` 的雅可比矩阵的奇异值， **Green-Lagrange** 张量 `[MYV93, ZMT05]` 或综合畸变度量 `[YYS06]` 上的。

$\quad$ Other improvements on the method of barycentric coordinates were proposed by Zayer et al. [ZRS05a, ZRS05b] and Yoshizawa et al. [YBS04], who showed how to dynamically adjust the barycentric weights such that the system converges to a parameterization minimizing stretch.

$\quad$ 对重心坐标方法的其他改进由 $Zayer$ 等人 `[ZRS05a, ZRS05b]` 和 $Yoshizawa$ 等人 `[YBS04]` 提出，他们展示了如何动态调整重心权重，从而使系统收敛到参数化最小化拉伸。

$\quad$ Another approach to parameterization is inspired by recent advances in dimension reduction and manifold learning [LYD*05, ZKK02]. The basic principle is to preserve some geometric property like geodesic distance of a higher dimensional data set while embedding it in a lower dimensional space. For example, Chen et al. [CLZW07] introduce a new parameterization technique based on local tangent space alignment (LTSA), which tries to embed each one-ring of the mesh in some optimal manner in the plane, and then solves a global linear system to "stitch" the one-rings together to one coherent triangle mesh. In this sense, it is the closest to the approach we describe in this paper.

$\quad$ 另一种参数化方法的灵感来自降维和流形学习的最新进展 `[LYD*05,ZKK02]` 。其基本原理是在将高维数据集嵌入低维空间的同时，保持像高维数据集的测地线距离等几何性质。例如，$Chen$ 等人 `[CLZW07]` 提出了一种新的基于局部切线空间对齐（ **LTSA** ）的参数化技术，该技术试图以某种最优方式将网格的每个1领域嵌入到平面中，然后求解一个全局线性系统，来将1领域“缝合”到一个相干的三角形网格中。从这个意义上说，它是最接近我们在本文中描述的方法。

$\quad$ A series of very recent works on conformal parameterizations by Yang et al. [YKL*08], Ben-Chen et al. [BCGB08] and Springborn et al. [SSP08] manipulate the curvature distribution on a 3D mesh, flattening it by migrating the total curvature so that it is distributed on only a small number of so-called "cone singularities". The other mesh vertices retain no curvature. For the case of a mesh having disk topology with a given boundary, this means concentrating the curvature on the boundary alone. In practice it amounts to computing new lengths for the mesh edges, so that they can be embedded in the plane. Once the 2D edge lengths are computed, the final 2D embedding is computed either by an incremental layout process, or by solving a simple sparse linear system (which happens to be identical to the LSCM process mentioned later in this paper, since that process reproduces a planar embedding). The difference between the three methods is the precise algorithm used to manipulate the curvature distribution. These methods, although designed to minimize only conformal (i.e. angular) distortion, in practice produce parameterizations with not too much stretch. They are also relatively easy to compute, thus are strong contenders for use in conformal parameterization scenarios.

$\quad$ $Yang$ 等人 `[YKL*08]` 、$Ben-Chen$等人 `[BCGB08]` 和 $Springborn$ 等人 `[SSP08] ` 最近在共形参数化方面进行了一系列工作，他们操纵了三维网格上的曲率分布，通过迁移总曲率使其扁平，使其仅分布在少数所谓的“锥奇点”上。其他网格顶点没有保留曲率。对于网格具有给定边界的圆盘拓扑的情况，这意味着只将曲率集中在边界上。在实践中，这相当于计算网格边缘的新长度，以便它们可以嵌入到平面中。一旦二维边缘长度被计算出来，最终的二维嵌入要么通过增量布局过程来计算，要么通过求解一个简单的稀疏线性系统来计算(这恰好与本文后面提到的 **LSCM** 过程相同，因为该过程复制了一个平面嵌入)。这三种方法的不同之处在于用于操纵曲率分布的具体算法。这些方法，虽然设计为了最小化共形（即角）失真，在实践中产生的参数化结果不会有太大的拉伸。它们也相对容易计算，因此是在共形参数化场景中使用的有力竞争者。

# 3 贡献

$\quad$ We apply the methodology of Sorkine and Alexa [SA07] for mesh editing (which has its origins in a series of papers starting with Sorkine et al. [SCOL*04]) to the problem of mesh parameterization. This poses the problem as that of finding optimal local transformations for each individual mesh element from an appropriate family and then "stitching" the transformed triangles together to a 2D mesh. As opposed to [SA07], where the local transformations are applied to one-rings of a vertex and its neighbors, we apply the local transformations to individual triangles. This then becomes a proper finite-element discretization of an associated continuous problem. In this context, our contributions are:

$\quad$ 我们将 $Sorkine$ 和 $Alexa$  `[SA07]` 的方法应用于网格编辑（它起源于 $Sorkine$ 等人 `[SCOL*04]` 开始的一系列论文）来处理网格参数化问题。这就产生了一个问题，即从合适的网格族中找到每个单独网格元素的最优局部转换，然后将转换后的三角形“缝合”到一个2D网格中。与局部变换应用于顶点的1领域及其邻居的 `[SA07]` 相反，我们将局部变换应用于单个三角形。这就变成了相关连续问题的适当的有限元离散化。在这方面，我们的贡献是:

+ For the case of local similarity transformations, our method is shown to be equivalent to the well known Least-Squares Conformal Mapping (LSCM) method [LPRM02].
+ 对于局部相似度变换的情况，我们的方法被证明等价于众所周知的最小二乘共形映射（ **LSCM** ）方法 `[LPRM02]` 。
+ For the case of local rotational transformations, we provide an efficient and simple iterative "local/global" algorithm to solve the problem. This leads to a parameterization which is close to isometric and shown to be superior to competing algorithms. Additionally, the algorithm minimizes an "intrinsic" deformation energy function that may be expressed in terms of the singular values of the Jacobian of the parameterization, as is the case for many other distortion measures. The algorithm is shown to be very fast, due to pre-factoring of the linear system involved in the global step, and optional parallel processing in the local phase.
+ 对于局部旋转变换，我们提供了一种高效、简单的迭代“局部/全局”算法来求解。这导致了一个接近等距的参数化，并显示优于竞争算法。此外，该算法最小化了可以用参数化雅可比矩阵的奇异值表示的“内在”变形能量函数，就像许多其他变形度量的情况一样。由于在全局步骤中涉及到线性系统的预分解，以及在局部阶段可选的并行处理，该算法的速度非常快。
+ We propose a more general "hybrid" parameterization model which provides a continuous spectrum of possibilities, controlled by a single parameter. The two cases described above (similarities and rotations) lie at the two ends of the spectrum. The hybrid parameterization may also be computed using a similar local/global algorithm.
+ 我们提出了一个更一般的“混合”参数化模型，它提供了一个由单个参数控制的连续的可能性谱。上面描述的两种情况（相似性和旋转）位于光谱的两端。混合参数化也可以使用类似的局部/全局算法来计算。

# 4 通用的局部/全局方法

$\quad$ If each triangle of the 3D triangle mesh were required to be flattened to the plane independently of the other triangles, this would certainly be easy. Requiring that all the flattened triangles fit together into one mesh with the correct orientations is the main challenge (see Figure 2). Obviously some of the triangles are going to be deformed in the process. Assume we allow each triangle to be deformed by some subset of the 2D linear transformations, in the sense that this transformation "does not count" as a deformation. For example, translations of the triangles are obviously allowed. A conformal parameterization would also allow each triangle to undergo a similarity transformation (only). An isometry would allow only a rotation. An authalic parameterization would allow only transformations with unit determinant.

$\quad$ 如果要求3D三角形网格中的每个三角形都被平到独立于其他三角形的平面上，这当然会很容易。要求所有的扁平三角形以正确的方向匹配到一个网格中是主要的挑战(参见图2)。显然，一些三角形在这个过程中会变形。假设我们允许每个三角形被二维线性变换的某些子集所变形，在这种意义上，这种变换“不计入”变形。例如，三角形的平移显然是允许的。共形参数化也允许每个三角形(仅)进行相似性变换。等距法只允许旋转。一个等体积的参数化将只允许具有单位行列式的转换。

![image-20220719132213703](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207191322744.png)

$\quad$ Assume the triangles of the 3D triangle mesh are numbered with $t=1$ to $T$ and the area of the 3D triangles are $A_t$ . Assume that each 3D triangle is equipped with its own local isometric parameterization using a triangle in the plane $x_t=\{x_t^0,x_t^1,x_t^2\}$ . Our goal is to find a single parameterization of the entire mesh, i.e., a piecewise linear mapping from the 3D mesh to the 2D plane, described by assigning 2D coordinates $u$ to each of the $n$ vertices. For triangle $t$, let us denote these 2D coordinates as $u_t=\{u_t^0,u_t^1,u_t^2\}$ . Given this setup, the mapping between $x_t$ and $u_t$ has an associated $2 \times 2$ Jacobian matrix which is constant per triangle. We denote this matrix at triangle $t$ as $J_t(u)$ to express its dependence on the $u$ . It represents the linear portion of the affine mapping from the triangle described by $x_t$ to the triangle described by $u_t$ . In our method, we will also assign an auxiliary linear transformation ( $2\times 2$  matrix)  $L_t$  to each triangle taken from some family of allowed transformations $M$ (in particular, we will consider, in turn, *M* to be the similarity transformations, and later, the rotations).

$\quad$ 设3D三角形网格中的三角形编号为 $t=1$ 到 $T$ ，3D三角形的面积为 $A_t$ 。假设每个3D三角形在平面 $x_t=\{x_t^0,x_t^1,x_t^2\}$ 上都有自己的局部等距参数化。我们的目标是找到整个网格的单一参数化，即从3D网格到2D平面的分段线性映射，通过将2D坐标 $u$ 分配给 $n$ 个顶点来描述。对于三角形 $t$ ，我们将这些2D坐标表示为 $u_t=\{u_t^0,u_t^1,u_t^2\}$ 。给定这个设置， $x_t$ 和 $u_t$ 之间的映射有一个相关的 $2 \times 2$ 雅可比矩阵，并且对每个三角形而言都是常数。我们将三角形 $t$ 处的这个矩阵表示为 $J_t(u)$ ，以表示它对 $u$ 的依赖关系。它表示从 $x_t$ 描述的三角形到 $u_t$ 描述的三角形的仿射映射的线性部分。在我们的方法中，我们还将给每个三角形分配一个辅助线性变换 （$2\times 2$ 矩阵）$L_t$ ，它来自于一些允许的变换族 $M$ （特别地，我们将反过来考虑， $M$ 是相似变换，然后是旋转）。

$\quad$ Define the energy of the parameterization coordinates $u$ and an auxiliary set of $T$ linear transformations $L=\{L_1,\dots,L_T\}$ to be

$\quad$ 定义参数化坐标 $u$ 和 $T$ 个线性变换的辅助集合 $L=\{L_1,\dots,L_T\}$ 的能量为
$$
E(u,L)=\sum_{t=1}^{T}A_t \|J_t(u)-L_t\|_F^2
$$
$\quad$ where $\|\cdot\|_F$ is the Frobenius norm. Following Pinkall and Polthier [PP93], this energy may be rewritten in terms of the coordinates $x$ and $u$ (instead of in terms of the Jacobians) in an explicit form (in terms of the mesh vertex coordinates):

$\quad$ 其中 $\|\cdot\|_F$ 是 $Frobenius$ 范数（ $\|X\|_F \overset{ref}{=} \sqrt{\sum_i\sum_jX_{i,j}^2}$ ）。 $Pinkall$ 和 $Polthier$  `[PP93]` 之后，这个能量可以用坐标 $x$ 和 $u$ （而不是用雅可比矩阵）以显式形式（用网格顶点坐标）重写:
$$
E(u,L)=\frac{1}{2} \sum_{t=1}^T\sum_{i=0}^2 \cot(\theta_t^i)\Big\|(u_t^i-u_t^{i+1})-L_t(x_t^i-x_t^{i+1}) \Big\|^2 \tag{1}
$$
$\quad$ where $\theta_t^i$ is the angle opposite the edge ( $x_t^i, x_t^{i+1}$ ) in the triangle whose vertices are $x_t$ and superscripts are all modulo 2. Note that some of the $u_t^i$ are identical, as they are shared by more than one triangle in the mesh.

$\quad$ 式中 $\theta_t^i$ 为三角形中边 ( $x_t^i, x_t^{i+1}$ ) 的对角，它的顶点为 $x_t$ ，另外上标均取模2的。请注意，有些  $u_t^i$  是相同的，因为它们被网格中的多个三角形共享。

$\quad$ We would like to solve the following optimization problem:

$\quad$ 我们想解决以下优化问题:
$$
(u,L)=\mathrm{argmin}_{(u,L)}\  E(u,L) \quad s.t.\ L_t \in M \tag{2}
$$
$\quad$ Namely, find a set of $n$ 2D coordinates $u$ for the mesh vertices and $T$ matrices $L_1,\dots,L_T$ in $M$ such that the Jacobians of the transformation from the given $x$ to the $u$ are closest to the $L_t$ .

$\quad$ 即，为网格顶点找到一组 $n$ 个2D坐标 $u$ 和 $T$ 个矩阵 $L_1,\dots,L_T$ ，得从给定 $x$ 到 $u$ 的变换的雅可比矩阵最接近于 $L_t$ 。

$\quad$ Although we solve for both $u$ and $L$ , in the end we are interested only in $u$ while $L$ plays an auxiliary role only. As we shall see below, in many cases, the optimal $u$ may be defined as that minimizing an energy function formulated in terms of the singular values of the Jacobians $J_t(u)$ . In the next sections, we will examine a number of interesting cases for $M$ and relate our energy functions to those.

$\quad$ 虽然我们同时求解 $u$ 和 $L$ ，但最终我们只对 $u$ 感兴趣，而 $L$ 只起辅助作用。正如我们将在下面看到的，在许多情况下，最优 $u$ 可以定义为最小化以雅可比矩阵 $J_t(u)$ 奇异值表示的能量函数。在下一节中，我们将研究一些关于 $M$ 的有趣案例，并将我们的能量函数与这些案例联系起来。

## 4.1  *L* 矩阵的最佳拟合

$\quad$ Suppose we are asked to approximate one $2\times 2$ matrix $J$ as best we can by another  $2\times 2$ matrix $L$, where $L$ is taken from a restricted set of transformations $M$ (we will consider in turn similarities and rotations) and where distance is measured using the Frobenius matrix norm. In other words:

$\quad$ 假设我们被要求用另一个 $2\times 2$ 矩阵 $J$ 尽可能地近似一个 $2\times2$ 矩阵 $L$ ，其中 $L$ 是从一个受限的转换集 $M$ 中取来的(我们将依次考虑相似性和旋转)，其中距离是使用 $Frobenius$ 矩阵范数测量的。换句话说:
$$
d(J,L)=\|J-L\|_F^2=tr\Big[(J-L)^T(J-L)  \Big]
$$
$\quad$ This problem can be solved using Procrustes analysis [GD04], and its solution in general is computed using the Singular Value Decomposition (SVD) of $J$ .

$\quad$ 这个问题可以用 $Procrustes$ 分析来解决 `[GD04]` ，其解一般是用 $J$ 的奇异值分解(SVD)来计算的。

$\quad$ In particular, using SVD,  $J$ may be written as

$\quad$ 特别地，使用SVD， $J$ 可以写成
$$
J=U\Sigma V^T
$$
$\quad$ where $U$ and $V$ are orthonormal, and $\Sigma$ is a diagonal matrix:  

$\quad$ 这里 $U$ 和 $V$ 是正交的， $\Sigma$ 是一个对角矩阵:
$$
\Sigma=\begin{pmatrix}
\sigma_1 & 0 \\
0 & \sigma_2
\end{pmatrix}
$$
$\quad$ We use here a "signed version" of the SVD, where the determinant of $UV^T$ is constrained to be positive, $\sigma_1$ is positive and $\sigma_2$ may be positive or negative. We refer to these $\sigma$ as signed singular values. This signed version is needed to constrain our Procrustes solutions to exclude orientation reversing transformations.

$\quad$ 我们在这里使用SVD的“有符号版本”，其中 $UV^T$ 的行列式被约束为正的，$\sigma_1$ 是正的， $\sigma_2$ 可以是正的或负的。我们称这些 $\sigma$ 为有符号的奇异值。需要这个有符号的版本来约束我们的 $Procrustes$ 解，以排除方向反转变换。

$\quad$ Given this decomposition, it is easy to show that the optimal rotation minimizing the distance $d(J,L)$ is obtained by setting both singular values to 1, i.e. $L=UV^T$ . Similarly, the optimal similarity transform is obtained by setting both singular values to $(\sigma_1+\sigma_2)/2$ . See Figure 3 for examples.

$\quad$ 根据这种分解，很容易看出，通过将两个奇异值都设为1，即 $L=UV^T$ ，就可以得到最小化距离 $d(J,L)$ 的最优旋转。同样，通过将两个奇异值设为 $(\sigma_1+\sigma_2)/2$ ，可以得到最优相似度变换。参见图3中的示例。

![image-20220719165443448](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207191654494.png)

## 4.2 As-similar-as-possible (ASAP) mappings  

$\quad$ Conformal mappings are those which preserve angles, which are invariant under similarity transformations. Thus, in order to produce a conformal-type parameterization, the family $M$ of allowed transformations should be similarities, which may be parameterized as all matrices of the form:

$\quad$ 共形映射是那些保持角度的映射，它们在相似变换下是不变的。因此，为了获得共形参数化，允许的变换的 $M$ 族应该是相似型矩阵，可以将其参数化为以下形式的所有矩阵:
$$
M=\begin{Bmatrix}
\begin{pmatrix}
a & b \\
-b & a
\end{pmatrix}:a,b\in \mathbf{R}
\end{Bmatrix} \tag{3}
$$
$\quad$ Thus we may represent the allowed $L_t$ in the energy function (2) with the variables $a=(a_1,\dots,a_T)$ ,  $b=(b_1,\dots,b_T)$ . Since the $x_t^i$ and $\theta_t^i$ are fixed, the energy function is quadratic in the variables $a,b,u$ and thus may be minimized by solving a large sparse linear system with these variables.

$\quad$ 因此，我们可以用变量 $a=(a_1，\dots,a_T)$ ， $b=(b_1，\dots,b_T)$ 表示能量函数(2)中允许的 $L_t$ 。由于 $x_t^i$ 和 $\theta_t^i$ 是固定的，能量函数在变量 $a,b,u$ 中是二次的，因此可以通过求解具有这些变量的大型稀疏线性系统来最小化。

$\quad$ Since we try to stay close to the family of similarity transformations, we call this parameterization "as-similaras-possible" (ASAP). Appendix A proves that solving (2) with this $M$ is equivalent to finding the $u$ that minimizes Lévy’s conformal energy:

$\quad$ 因为我们试图保持接近相似转换簇，所以我们将此参数化称为“as-similaras-possible”(ASAP)。附录A证明用这个 $M$ 解(2) 等价于找到使 $\mathrm{L\acute{e}vy}$ 的共形能量最小的 $u$ :
$$
\sum_{t=1}^TA_t(\sigma_{1,t}-\sigma_{2,t})^2
$$
$\quad$ where $\sigma_{1,t}$ and $\sigma_{2,t}$ are the signed singular values of $J_t$ – the Jacobian of the t-th triangle’s transformation. Since the Least-Square Conformal mapping (LSCM) technique [LPRM02] also minimizes precisely this energy, the two techniques are equivalent.

$\quad$ 其中 $\sigma_{1,t}$ 和 $\sigma_{2,t}$ 是 $J_t$ 的带符号奇异值——第t个三角变换的雅可比矩阵。由于最小二乘共形映射( **LSCM** )技术 `[LPRM02]` 也精确地最小化这一能量，两种技术是等价的。

$\quad$ As with LSCM, for non-developable meshes, the (trivial) solution that collapses all of the vertices to a single point in the plane achieves a global minimum – zero energy. This can be avoided by constraining two vertices to two different locations in the plane. In practice, we pin down the two vertices most distant from each other (the diameter) in the mesh.

$\quad$ 与 **LSCM** 一样，对于非可展网格，将所有顶点折叠到平面上单个点的(平凡)解获得了全局最小值——零能量。这可以通过将两个顶点限制在平面的两个不同位置来避免。在实践中，我们固定网格中相距最远的两个顶点(直径)。

## 4.3 As-rigid-as-possible (ARAP) mappings  

$\quad$ While conformal mappings have many nice mathematical properties, they are not always exactly what the application needs. The fact that arbitrary scaling factors may creep into the parameterization makes it unsuitable for applications which try to minimize "stretch" and preserve the proportions of the triangles.

$\quad$ 虽然共形映射有许多很好的数学性质，但它们并不总是应用程序所需要的。事实上，任意的缩放因子可能会渗入参数化，这使得它不适合那些试图最小化“拉伸”和保持三角形比例的应用程序。

$\quad$ To obtain an "as-rigid-as-possible" mapping we limit the family of allowed local transformations to be just rotations:

$\quad$ 为了获得一个“尽可能严格”的映射，我们将允许的局部转换系列限制为仅仅是旋转:
$$
M = \begin{Bmatrix}
\begin{pmatrix}
\cos\theta  &  \sin\theta \\
-\sin\theta  &  \cos\theta
\end{pmatrix}
: \theta \in [0,2\pi)
\end{Bmatrix}
$$
$\quad$ Or, in other words, the same as (3), only with the extra requirement that a2 +b2 = 1.  

$\quad$ 或者换句话来说，和 (3) 一样，只是有一个额外的要求，即 $a^2+b^2=1$ 。

$\quad$ Appendix A proves that solving (2) with this $M$ is equivalent to finding the $u$ which minimizes 

$\quad$ 附录A证明用这个 $M$ 解 (2) 等价于找到了 $u$ 使得下面这个式子最小
$$
\sum_{t=1}^T A_t\Big[ (\sigma_{1,t}-1)^2+(\sigma_{2,t}-1)^2 \Big]
$$
$\quad$ This energy is similar to the Green-Lagrange energy [MYV93, ZMT05], which uses terms of the form $\Big[(\sigma_{1,t}^2-1)^2+(\sigma_{2,t}^2-1)^2  \Big]$ and also produces parameterizations which are close to isometric.

$\quad$ 这个能量类似于 $Green-Lagrange$ 能量 `[MYV93, ZMT05]` ，它使用形式 $\Big[(\sigma_{1,t}^2-1)^2+(\sigma_{2,t}^2-1)^2 \Big]$ ，也产生接近等距的参数化。

$\quad$ Alas, the extra condition on $L_t$ in (1) means that the energy function may no longer be minimized by solving a linear system.

$\quad$ 遗憾的是，(1) 中 $L_t$ 的附加条件意味着可能不再能通过解线性系统使能量函数最小化。

## 4.4. Local/Global Algorithm

$\quad$ To solve the minimization problem (2) for an ARAP mapping, we adapt the local/global algorithm of [SA07]. This iterates between two phases. In the first *local* phase, the optimal rotation $L_t$ is computed per triangle, assuming the $u$ are fixed. Then, in the second *global* phase, the $L_t$ are assumed fixed, and the optimal $u$ are solved for as a sparse linear system. (Recall that $x_t$ are fixed throughout the algorithm.) Since each step is guaranteed to reduce the energy, this energy will eventually converge. Additionally, since the matrix of the global phase is unchanged from iteration to iteration, it only has to be factored once and reused at each iteration.

$\quad$ 为了解决 **ARAP** 映射的最小化问题 (2) ，我们采用了 `[SA07]` 的局部/全局算法。这在两个阶段之间迭代。在第一个局部阶段，假设 $u$ 是固定的，每个三角形计算最优旋转 $L_t$ 。然后，在第二个全局阶段，假设 $L_t$ 是固定的，并将最优 $u$ 作为一个稀疏线性系统求解。(回想一下， $x_t$ 在整个算法中是固定的。)因为每一步都保证会减少能量，所以这些能量最终会聚合。此外，由于全局阶段的矩阵在每次迭代中都是不变的，它只需要分解一次并在每次迭代中重用。

### 4.4.1 Local Phase

$\quad$ The local phase can be solved using the SVD factorization of $J$ as described in Section 4.1. Equivalently, and analogously to [SA07], for ARAP one can also perform the SVD factorization directly on the following "cross-covariance" matrix in place of $J_t(u)$

$\quad$ 局部阶段可以用第4.1节所述的 $J$ 的 **SVD** 分解来求解。同样地，类似于 `[SA07]`，对于 **ARAP** ，人们也可以直接对下面的“交叉协方差”矩阵进行 **SVD** 分解，以代替 $J_t(u)$
$$
S_t(u) = \sum_{i=0}^2 \cot(\theta_t^i)(u_t^i-u_t^{i+1})(x_t^i-x_t^{i+1})^T
$$
### 4.4.2 Global Phase

$\quad$ For fixed $L_t$ , the energy $E(u,L)$ is quadratic in $u$ . The minimum $u$ can be found by setting the gradients of (1) to zero and solving the associated linear system. To calculate this, overloading the notation slightly, we rewrite the energy function in terms of the mesh half-edges:

$\quad$ 对于固定 $L_t$ ，能量 $E(u,L)$ 是$u$的二次元。最小 $u$ 可以通过将 (1) 的梯度设为零并求解相关的线性系统来找到。为了计算这个，稍微重载一下符号，我们用网格半边重写了能量函数:
$$
\begin{aligned}
E(u,L) &= \frac{1}{2}\sum_{t=1}^T\sum_{i=0}^2\cot(\theta_t^i)\Big\| (u_t^i-u_t^{i+1})-L_t(x_t^i-x_t^{i+1}) \Big\| ^2  \\
&= \frac{1}{2}\sum_{(i,j)\in he}\cot(\theta_{ij})\Big\| (u_i-u_j)-L_{t(i,j)}(x_i-x_j) \Big\| ^2
\end{aligned}
$$
$\quad$ where $he$ is the set of half-edges in the mesh, $u_i$ and $x_i$ are coordinates of vertices $i$ , $t(i,j)$ is the triangle containing the half-edge $(i,j)$ , and $\theta_{ij}$ is the angle opposite $(i,j)$ in $t(i,j)$ .

$\quad$ 其中 $he$ 是网格中半边的集合， $u_i$ 和 $x_i$ 是顶点 $i$ 的坐标， $t(i,j)$ 是包含半边 $(i,j)$ 的三角形， $\theta_{ij}$ 是 $t(i,j)$ 中 $(i,j)$ 的对角。

$\quad$ Setting the gradient to zero, we obtain the following set of linear equations for $u$ .
$$
\sum_{j\in N(i)}[\cot(\theta_{ij})+\cot(\theta_{ji})](u_i-u_j) \\
= \sum_{j\in N(i)}[\cot(\theta_{ij})L_{t(i,j)}+\cot(\theta_{ji})L_{t(j,i)}](x_i-x_j), \tag{4}\\
\forall \, i = 1,\cdots,n.
$$
$\quad$ The entries of the associated matrix depend only on the geometry of the input 3D mesh. Thus this sparse matrix is fixed throughout the algorithm, allowing us to pre-factor it (e.g. with Cholesky decomposition) [GvL05, In0] and reuse the factorization many times throughout the algorithm in order to accelerate the process. This has a significant impact on algorithm efficiency.

$\quad$ 相关矩阵的条目仅依赖于输入的3D网格的几何形状。因此，这个稀疏矩阵在整个算法中是固定的，允许我们对其进行预分解(如 $Cholesky$ 分解) `[GvL05, In0]` ，并在整个算法中多次重用该分解，以加快过程。这对算法的效率有很大的影响。

$\quad$ Unfortunately, stitching the triangles using a global Poisson equation may result in some triangles "flipping" their orientation especially for a highly curved surface with compact boundary. We solve this with a final post-processing phase, e.g., the "convex virtual boundary" algorithm of Karni et al. [KGG05]. Since in most cases, there are only a few flips, sprinkled throughout the parameterization, the postprocessing solves the flips without changing much else.

$\quad$ 不幸的是，使用全局泊松方程拼接三角形可能会导致一些三角形“翻转”它们的方向，特别是对于边界紧凑的高度弯曲的曲面。我们用最后的后处理阶段来解决这个问题，例如 $Karni$ 等人 `[KGG05]` 的“凸虚拟边界”算法。因为在大多数情况下，只有几次翻转，散布在整个参数化过程中，后处理解决了这些翻转，而没有改变太多其他东西。



## 4.5 The initial parameterization  

$\quad$ Our local/global algorithm requires an initial parameterization $M$ to start it off. The basic requirement from the initial parameterization is that it be a valid embedding (contain no flips) reasonably close to a parameterization with not too much distortion, and be fast to generate. Candidates are the shape-preserving method [Flo97] and LSCM [LPRM02] as they can be computed quickly. We found the shapepreserving parameterization more suitable for meshes with one boundary, and LSCM [LPRM02] for meshes with multiple boundaries. The experimental results shown in Section 6 are obtained using these initial parameterizations.

$\quad$ 我们的局部/全局算法需要初始化参数 $M$ 来开始。初始参数化的基本要求是，它是一个有效的嵌入(不包含翻转)，合理地接近一个参数化，不存在太多失真，并且生成速度快。候选方法是形状保持法 `[Flo97]` 和 `LSCM [LPRM02]` ，因为它们可以快速计算。我们发现形状保持参数化方法更适用于单边界网格，而 **LSCM**  `[LPRM02]` 则更适用于多边界网格。第6节所示的实验结果是使用这些初始参数得到的。

$\quad$ We tested the sensitivity of our algorithm to different types of $M$’s, as mentioned above. We found that the algorithm is not sensitive to $M$ at all. Figure 4 shows the progress of the iterative algorithm when initialized with the shapepreserving parameterization and LSCM. Both converge fast and stably.

$\quad$ 如上所述，我们测试了算法对不同类型的 $M$ 的敏感性。我们发现该算法对 $M$ 完全不敏感。图4显示了使用保持形状参数化和 **LSCM** 初始化迭代算法的进展。两者收敛快且稳定。

![image-20220720113206310](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207201132396.png)

# 5 混合模型

$\quad$ Our ASAP parameterization belongs to the family of (approximately) conformal maps and may be computed easily by solving a simple linear system. However, it is not the most area-preserving among the conformal parameterizations, and, in fact, the non-linear ABF++ method preserves area much better, while still being approximately conformal. On the other hand, our ARAP parameterization preserves areas much better, but since it it strives to be isometric, it might damage the conformality in this effort. We now present an energy function which is a generalization of (1), which provides a means to generate a parameterization anywhere between ASAP and ARAP. The two latter are endpoints of the spectrum, and the result is controlled by a parameter $\lambda \in[0, \infty)$.

$\quad$ 我们的 **ASAP** 参数化属于(近似)共形映射族，通过求解一个简单的线性系统可以很容易地计算出来。然而，它并不是最保面积的共形参数化，事实上，非线性的 **ABF++** 方法在近似保形的同时有着更好的保面积的效果。另一方面，我们的      **ARAP** 参数化能更好地保面积，但由于它努力保持等距，它可能会破坏共形性。现在我们提出一个能量函数，它是 (1) 的推广，它提供了一种在 **ASAP** 和 **ARAP** 之间产生参数化结果的方法。后两个是频谱的端点，结果由参数 $\lambda \in[0, \infty)$ 控制。

$\quad$ The hybrid energy function is  

$\quad$ 混合能量函数为
$$
E(u,a,b) = \frac{1}{2}\sum_{t=1}^T\Bigg[\sum_{i=0}^2  \cot(\theta_t^i)\Big\|\nabla e_t^i \Big\|^2 + \lambda(a_t^2+b_t^2-1)^2 \Bigg], \tag{5} \\
$$
$\quad$ where

$\quad$ 其中
$$
\nabla e_t^i  = (u_t^i-u_t^{i+1}) - \begin{pmatrix}
a_t & b_t \\
-b_t & a_t
\end{pmatrix} (x_t^i - x_t^{i+1}).
$$
$\quad$ Setting $\lambda=0$ will be equivalent to ASAP while a very large value of $\lambda$ will be equivalent to ARAP. Any value inbetween will yield an intermediate parameterization, so the user may control the tradeoff between conformality and area-preservation.

$\quad$ 设置 $\lambda=0$ 将等价于 **ASAP** ，而一个非常大的值 $\lambda$ 将等价于 **ARAP** 。任何介于两者之间的值都将产生一个中间参数，因此用户可以控制保形和保面积之间的权衡。

$\quad$ Solving for the parameterization coordinates $u$ which minimize $E(u,a,b)$ involves solving also for the auxiliary vectors of unknowns of the similarity transformations $a$ and $b$ . The value of $\lambda$ indicates how much we want to force the similarity to be a rotation. A local/global algorithm similar to that we use for solving for the ARAP parameterization may be used here as well, i.e. iterate while alternating between two phases: one local and one global. Recall that $x$ is fixed (derived directly from the input 3D mesh). The local phase keeps the parameterization coordinates $u$ fixed and solves for the optimal $a_t$ and $b_t$ per triangle $t$ . Examination of (5) reveals that this involves solving two cubic equations in $a_t$ and $b_t$ . Furthermore, this reduces to a single cubic equation in $a_t$ , (Equation (B3) in Appendix B), which may be solved analytically. The global phase keeps both vectors $a$ and $b$ fixed and solves a global sparse linear system (similar to (4)) for $u$ . Since the matrix of the linear system is fixed throughout all iterations, it may be pre-factored at the beginning, and reused in all iterations thereafter. Thus the runtime of the procedure is dominated by the first iteration. This makes for a simple and efficient algorithm.

$\quad$ 解参数化坐标 $u$ ，使 $E(u,a,b)$ 最小，还涉及解 $a$ 和 $b$ 相似变换的未知辅助向量。 $\lambda$ 的值表示我们希望将相似性强制为旋转的程度。这里也可以使用类似于我们用于求解 **ARAP** 参数化的局部/全局算法，即在两个阶段交替迭代：一个局部阶段和一个全局阶段。回想一下， $x$ 是固定的(直接从输入的3D网格派生)。局部阶段保持参数化坐标 $u$ 固定，然后逐三角形 $t$ 求解最优 $a_t$ 和 $b_t$ 。对 (5) 的检验表明，这涉及到求解 $a_t$ 和 $b_t$ 中的两个三次方程。进一步简化为 $a_t$ 中的一个三次方程(附录B中的 (B3) 式)，可以用解析法求解。全局阶段保持向量 $a$ 和 $b$ 固定，求解 $u$ 的全局稀疏线性系统(类似于 (4) )。由于线性系统的矩阵在所有迭代中都是固定的，所以可以在开始时对其进行预分解，并在之后的所有迭代中重用。因此，过程的运行时间由第一次迭代决定。这就形成了一个简单而有效的算法。

# 6 实验结果与对比

$\quad$ We have applied our approach to parameterize a variety of 3D meshes and compared with other relevant methods.  These include LSCM (equivalent to our ASAP method) [LPRM02], direct ABF++ (ABF++ without the hierarchical solver) [SLMB05], which we label dABF++, linear ABF [ZLS07], which we label LABF, inverse curvature [YKL*08], which we label IC, and curvature prescription [BCGB08], which we label CP. We show some results in Fig. 1 and Figs. 5-8.  In our algorithm, we used the sparse Cholesky linear solver [In0] for the global systems and the analytic solution to Equation (B3) for the local systems.  The IC results were kindly provided by Yang and the CP results by Ben-Chen, the authors of those methods, who ran their own software.  The results of LABF where obtained by running software kindly provided by Zayer.

$\quad$ 我们将该方法应用于各种三维网格的参数化，并与其他相关方法进行了比较。这包括 **LSCM** (等同于我们的 **ASAP** 方法) `[LPRM02]` ，直接 **ABF++** (不带层次解算器的 **ABF++** ) `[SLMB05]` ，我们标记为 **dABF++** ，线性 **ABF**  `[ZLS07]` ，我们标记为 **LABF** ，反曲率 `[YKL*08]` ，我们标记为 **IC** ，曲率处方 `[BCGB08]` ，我们标记为 **CP** ，我们在图1和图5-8中展示了一些结果。在我们的算法中，我们对全局系统使用稀疏 $Cholesky$ 线性解 `[In0]` ，对局部系统使用方程 (B3) 的解析解。 **IC** 结果由Yang提供，**CP** 结果由Ben-Chen提供，他们是这些方法的作者，使用他们自己的软件。 **LABF** 的结果是通过Zayer提供的软件得到的。

![image-20220720123641906](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207201236978.png)

![image-20220720123656502](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207201236585.png)

![image-20220720123706256](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207201237325.png)

![image-20220720123714637](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207201237692.png)



$\quad$ Computing the ASAP parameterization involves the solution of one sparse linear system, thus is very fast. Computing ARAP involves running the local/global algorithm. This converged in up to 10 iterations in all our experiments. Computing the hybrid also involves an iterative local/global algorithm, but with the local phase using the analytic solution to Equation (B3) instead of a simple $2\times 2$ SVD operation.

$\quad$ **ASAP** 参数化的计算涉及到一个稀疏线性系统的解，因此非常快。计算 **ARAP** 需要运行本地/全局算法。在我们所有的实验中，这收敛了多达10次迭代。计算混合算法还涉及到一个迭代的局部/全局算法，但局部阶段使用方程 (B3) 的解析解，而不是简单的 $2\times 2$ **SVD** 操作。

$\quad$ The figures show the parameterizations resulting from ASAP, ARAP and the hybrid method with some interesting values of $\lambda$ . These are compared with the results of the other algorithms. The runtime of our local/global procedure is comparable to the state-of-the-art ABF++. Our local/global parameterization method may be applied also to meshes with multiple boundaries. Fig. 8 shows one such result. The LABF method is not applicable to such inputs.

$\quad$ 图中显示了参数化产生的 **ASAP** , **ARAP** 和混合方法与一些有趣的值 $\lambda$ 。并与其他算法的结果进行了比较。我们的局部/全局过程的运行时可与最先进的 **ABF++** 相媲美。局部/全局参数化方法也适用于多边界网格。图8显示了一个这样的结果。 **LABF** 方法不适用于这种输入。

$\quad$ To quantify the parameterization distortion, we compute both the angle and area distortion metric defined using the signed singular values $\sigma_{1,t}$ and $\sigma_{2,t}$ of the Jacobians $J_t$ for each triangle, as defined in [HG99, DMK03]:

$\quad$ 为了量化参数化失真，我们计算了使用雅可比矩阵 $J_t$ 的带符号奇异值 $\sigma_{1,t}$ 和 $\sigma_{2,t}$ 定义的角度和面积失真度量，定义在  `[HG99, DMK03]` 中:
$$
D^{\mathrm{angle}} = \sum_t \rho_t \Big( \sigma_t^1/\sigma_t^2  + \sigma_t^2/\sigma_t^1 \Big) \\
D^{\mathrm{area}} = \sum_t \rho_t \Big( \sigma_t^1\sigma_t^2  + 1/\sigma_t^1\sigma_t^2 \Big) 
$$
$\quad$ where the weight $\rho_t$ is  

$\quad$ 其中权重 $\rho_t$ 是
$$
\rho_t = A_t/\sum_tA_t
$$
$\quad$ and $A_t$ is the area of triangle $t$ . The values of the distortion measures obtained by the various algorithms is summarized in Table 1. As is evident in the table, our ARAP parameterization consistently gives the best value of $D^{\mathrm{area}}$ , at a very small, even insignificant, penalty in $D^{\mathrm{angle}}$ . It is possible to significantly improve the value of $D^{\mathrm{area}}$  relative to LSCM even by introducing a small value of $\lambda$ .

$\quad$ $A_t$ 是三角形 $t$ 的面积。各种算法得到的畸变测量值如表1所示。如表中所示，我们的 **ARAP** 参数化一致地给出了 $D^{\mathrm{area}}$ 的最佳值，在 $D^{\mathrm{angle}}$ 中有一个非常小的，甚至是微不足道的代价。即使引入一个很小的 $\lambda$ 值，也有可能显著提高 $D^{\mathrm{area}}$  相对于 **LSCM** 的值。

![image-20220720123740164](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207201237219.png)

# 7 讨论和结论

$\quad$ We have presented a novel approach to parameterization of 3D mesh surfaces, by minimizing a very general energy function. We have also provided a simple and efficient local/global algorithm for computing these parameterizations. The local component of the algorithm tries to minimize distortion of the individual 2D triangles relative to the original 3D mesh geometry, while the global component guarantees that the resulting 2D triangles fit together in a coherent manner. Both phases may be computed efficiently, the local one taking advantage of parallelism (possibly on the GPU), and the global one taking advantage of efficient sparse linear solvers with factorization.

$\quad$ 我们提出了一种新的方法来参数化三维网格表面，通过最小化一个非常通用的能量函数。我们还提供了一个简单有效的局部/全局算法来计算这些参数化。该算法的局部部分试图将单个二维三角形相对于原始3D网格几何图形的失真降至最低，而全局部分则确保生成的二维三角形以连贯的方式匹配在一起。这两个阶段都可以有效地计算，局部阶段利用并行性(可能在GPU上)，全局阶段利用高效的稀疏线性分解求解器。

$\quad$ Our local/global algorithm embodies the motif "think globally, act locally", which is emerging as a powerful technique in geometry processing. This paper and others [DG07] have applied this to the problem of mesh parameterization and future work will address other applications where the technique may also be very effective.

$\quad$ 我们的局部/全局算法体现了“全局思考，局部行动”的主题，这是一种强大的几何处理技术。这篇论文和其他论文 `[DG07]` 将这一技术应用于网格参数化问题，未来的工作将解决其他应用，在这些应用中该技术可能也非常有效。



# 鸣谢

$\quad$ Thanks to Yongliang Yang and Miri Ben-Chen for providing results of the algorithms of [YKL*08] and [BCGB08]. Thanks also to Hugues Hoppe for his many helpful insights on this topic. This work is supported by National Natural Science Foundation of China (grants # 60776799, 60503067). Craig Gotsman and Steven Gortler were partially supported by United States - Israel Binational Science Foundation grant # 2006089.

$\quad$ 感谢杨永亮和Miri Ben-Chen提供 `[YKL*08]` 和 `[BCGB08]` 算法的结果。也感谢Hugues Hoppe在这个话题上提供了许多有益的见解。本研究得到了国家自然科学基金(资助号:60776799、60503067)的资助。Craig Gotsman和Steven Gortler得到了美国-以色列两国科学基金会2006089号拨款的部分支持。

# 引用

`[BCGB08]` BEN-CHEN M., GOTSMAN C., BUNIN G.: Conformal flattening by curvature prescription and metric scaling. *Computer Graphics Forum 27*, 2 (2008), 449–458. (Proc. Eurographics 2008). 2, 7, 9



`[CLZW07]` CHEN Z. G., LIU L. G., ZHANG Z. Y., WANG G. J.: Surface parameterization via aligning optimal local flattening. In *Proc. Symposium on Solid and Physical Modeling* (2007), pp. 291–296. 2



`[DG07]` DONG S., GARLAND M.: Iterative methods for improving mesh parameterizations. In Proc. IEEE Shape Modeling International (2007), pp. 119–210. 9  



`[DMA02]` DESBRUN M., MEYER M., ALLIEZ P.: Intrinsic parameterization of surface meshes. *Computer Graphics Forum 21*, 3 (2002), C209–C218. (Proc. Eurographics’02). 2



`[DMK03]` DEGENER P., MESETH J., KLEIN R.: An adaptable surface parameterization method. In *Proc. of 12th International Meshing Roundtable* (2003), pp. 227–237. 8



`[EDD*95]` ECK M., DEROSE T., DUCHAMP T., HOPPE H., LOUNSBERY M., STUETZLE W.: Multiresolution analysis of arbitrary meshes. In *Proc. Siggraph’95* (1995), pp. 173–182. 2



`[FH05]` FLOATER M. S., HORMANN K.: Surface parameterization: a tutorial and survey. In *Advances in Multiresolution for Geometric Modeling* (2005), pp. 157–186. 2



`[Flo97]` FLOATER M. S.: Parameterization and smooth approximation of surface triangulations. Computer Aided Geometry Design 14 (1997), 231–250. 2, 5  



`[Flo03]` FLOATER M.: Mean value coordinates. *Computer Aided Geometric Design 20*, 1 (2003), 19–27. 2



`[GD04]` GOWER J. C., DIJKSTERHUIS G. B.: Procrustes Problems. Oxford University Press, 2004. 4  



`[GvL05]` GOLUB G. H., VAN LOAN C. F.: *Matrix Computation*. Johns Hopkins Studies in Mathematical Sciences, 2005. 5



`[HG99]` HORMANN K., GREINER G.: MIPS: an efficient global parameterization method. In *Proc. Curves and Surfaces* (1999), pp. 153–162. 2, 8



`[IMH05]` IGARASHI T., MOSCOVICH T., HUGHES J. F.: Asrigid-as-possible shape manipulation. *ACM TOG 24*, 3 (2005), C1134–C1141. (Proc. Siggraph’05). 2



`[In0]` Intel math kernel library. http://developer.intel.com. 5, 7



`[KGG05]` KARNI Z., GOTSMAN C., GORTLER S. J.: Freeboundary linear parameterization of 3D meshes in the presence of constraints. In *Proc. IEEE Shape Modeling and Applications* (2005), pp. 268–277. 2, 5



`[LKL02]` LEE Y., KIM H. S., LEE S.: Mesh parameterization with a virtual boundary. *Computer and Graphics 26*, 5 (2002), 677–686. 2



`[LPRM02]` LÉVY B., PETITJEAN S., RAY N., MAILLOT J.: Least squares conformal maps for automatic texture atlas generation. *ACM TOG 21*, 3 (2002), C362–C371. (Proc. Siggraph’02). 2, 3, 4, 5, 6, 10



`[LYD*05]` LIU Y. S., YU P. Q., DU M. C., YONG J. H., ZHANG H., PAUL J. C.: Mesh parameterization for an open connected surface without partition. In *Proc. of Computer Aided Design and Computer Graphics* (2005), pp. 306–312. 2



`[MYV93]` MAILLOT J., YAHIA H., VERROUST A.: Interactive texture mapping. In *Proc. Siggraph’93* (1993), pp. 27–34. 2, 5



`[PP93]` PINKALL U., POLTHIER K.: Computing discrete minimal surface and their conjugates. *Experimental Mathematics 2*, 1 (1993), 15–36. 2, 3



`[SA07]` SORKINE O., ALEXA M.: As-rigid-as-possible surface modeling. In *Proc. Eurographics Symposium on Geometry Processing* (2007), pp. 109–116. 2, 3, 5



`[SCOL*04]` SORKINE O., COHEN-OR D., LIPMAN Y., ALEXA M., ROESSL C., SEIDEL H.-P.: Laplacian surface editing. In *Proc. Eurographics Symposium on Geometry Processing* (2004), pp. 175–184. 3



`[SdS00]` SHEFFER A., DE STURLER E.: Parameterization of faceted surfaces for meshing using angle-based flattening. *Engineering with Computer 17*, 3 (2000), 326–337. 2

