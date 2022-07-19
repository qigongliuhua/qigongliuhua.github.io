> **A Local/Global Approach to Mesh Parameterization**



# 摘要

$\quad$ We present a novel approach to parameterize a mesh with disk topology to the plane in a shape-preserving manner. Our key contribution is a local/global algorithm, which combines a local mapping of each 3D triangle to the plane, using transformations taken from a restricted set, with a global "stitch" operation of all triangles, involving a sparse linear system. The local transformations can be taken from a variety of families, e.g. similarities or rotations, generating different types of parameterizations. In the first case, the parameterization tries to force each 2D triangle to be an as-similar-as-possible version of its 3D counterpart. This is shown to yield results identical to those of the LSCM algorithm. In the second case, the parameterization tries to force each 2D triangle to be an as-rigid-as-possible version of its 3D counterpart. This approach preserves shape as much as possible. It is simple, effective, and fast, due to pre-factoring of the linear system involved in the global phase. Experimental results show that our approach provides almost isometric parameterizations and obtains more shape-preserving results than other state-of-the-art approaches. 

$\quad$ 我们提出了一种新方法，以保形方式将具有圆盘拓扑的网格参数化到平面。我们的主要贡献是一种局部/全局算法，该算法使用从受限集获取的变换，将每个 $3D$ 三角形的局部映射结合到平面，并对所有三角形进行全局“缝合”操作，涉及稀疏线性系统。局部变换可以来自各种族，例如相似性或旋转，生成不同类型的参数化。在第一种情况下，参数化试图强制每个 $2D $三角形成为其 $3D$ 对应物的尽可能相似的版本。结果表明，这可以得到与 $LSCM$ 算法相同的结果。在第二种情况下，参数化试图强制每个二维三角形成为其三维对应物的尽可能保刚性的版本。这种方法尽可能地保持形状。由于全局相位中涉及的线性系统的预分解，该方法简单、有效、快速。实验结果表明，与其他最先进的方法相比，我们的方法提供了几乎等距的参数化，并获得了更多的保形结果。

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





















