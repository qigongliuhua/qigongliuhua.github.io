> **Poisson Surface Reconstruction  **



# Abstract

*We show that surface reconstruction from oriented points can be cast as a spatial Poisson problem. This Poisson formulation considers all the points at once, without resorting to heuristic spatial partitioning or blending, and is therefore highly resilient to data noise. Unlike radial basis function schemes, our Poisson approach allows a hierarchy of locally supported basis functions, and therefore the solution reduces to a well conditioned sparse linear system. We describe a spatially adaptive multiscale algorithm whose time and space complexities are proportional to the size of the reconstructed model. Experimenting with publicly available scan data, we demonstrate reconstruction of surfaces with greater detail than previously achievable.*

*我们表明，从定向点重构曲面可以看作是一个空间泊松问题。这种泊松公式一次考虑所有点，而不诉诸启发式空间划分或混合，因此对数据噪声有很高的弹性。与径向基函数方案不同，我们的泊松方法允许局部支持基函数的层次结构，因此解可以简化为一个条件良好的稀疏线性系统。我们描述了一种空间自适应多尺度算法，其时间和空间复杂性与重构模型的大小成正比。通过对公开的扫描数据进行实验，我们展示了比以前细节更丰富的表面重建*



# 1. Introduction

Reconstructing 3D surfaces from point samples is a well studied problem in computer graphics. It allows fitting of scanned data, filling of surface holes, and remeshing of existing models. We provide a novel approach that expresses surface reconstruction as the solution to a Poisson equation.

从点样本重建三维曲面是计算机图形学中研究较多的问题。它允许扫描数据的拟合、表面孔洞的填充和现有模型的重构网格。我们提供了一种新颖的方法，将曲面重构表示为泊松方程的解。

Like much previous work (Section 2), we approach the problem of surface reconstruction using an implicit function framework. Specifically, like [Kaz05] we compute a 3D *indicator function* $\mathcal{X}$ (defined as 1 at points inside the model, and 0 at points outside), and then obtain the reconstructed surface by extracting an appropriate isosurface.

像许多以前的工作(第2节)一样，我们使用隐式函数框架来解决曲面重建的问题。具体来说，如[Kaz05]，我们计算一个3D *指示函数*  $\mathcal{X}$ (定义为模型内部点为1，外部点为0)，然后通过提取适当的等值面得到重构曲面。

Our key insight is that there is an integral relationship between oriented points sampled from the surface of a model and the indicator function of the model. Specifically, the gradient of the indicator function is a vector field that is zero almost everywhere (since the indicator function is constant almost everywhere), except at points near the surface, where it is equal to the inward surface normal. Thus, the oriented point samples can be viewed as samples of the gradient of the model’s indicator function (Figure 1).

我们的关键见解是，从模型表面采样的定向点与模型的指标函数之间存在一个整体关系。具体来说，指示器函数的梯度是一个几乎处处为零的向量场(因为指示器函数几乎处处为常数)，除了在靠近表面的点，在那里它等于向内表面法线。因此，定向点样本可以看作是模型指标函数梯度的样本(图1)。

> 二维泊松重建的直观说明

![image-20220810120120171](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208101201244.png)



The problem of computing the indicator function thus reduces to inverting the gradient operator, i.e. finding the scalar function $\mathcal{X}$ whose gradient best approximates a vector field $\vec{V}$ defined by the samples, i.e. $\min_\mathcal{X}\|\nabla \mathcal{X} - \vec{V}\|$ . If we apply the divergence operator, this variational problem transforms into a standard Poisson problem: compute the scalar function $\mathcal{X}$ whose Laplacian (divergence of gradient) equals the divergence of the vector field $\vec{V}$ ,

因此，计算指标函数的问题简化为反求梯度运算符，即找到标量函数 $\mathcal{X}$ ，其梯度最接近由样本定义的向量场 $\vec{V}$ ，即 $\min_\mathcal{X}\|\nabla \mathcal{X} - \vec{V}\|$ 。如果我们应用散度算子，这个变分问题转化为一个标准的泊松问题:计算标量函数 $\mathcal{X}$ ，其拉普拉斯(梯度散度)等于向量场 $\vec{V}$ 的散度，
$$
\nabla \mathcal{X} \equiv  \nabla \cdot \nabla  \mathcal{X} = \nabla \cdot \vec{V}
$$
We will make these definitions precise in Sections 3 and 4.

 我们将在第3节和第4节中精确地给出这些定义。

Formulating surface reconstruction as a Poisson problem offers a number of advantages. Many implicit surface fitting methods segment the data into regions for local fitting, and further combine these local approximations using blending functions. In contrast, Poisson reconstruction is a global solution that considers all the data at once, without resorting to heuristic partitioning or blending. Thus, like radial basis function (RBF) approaches, Poisson reconstruction creates very smooth surfaces that robustly approximate noisy data. But, whereas ideal RBFs are globally supported and nondecaying, the Poisson problem admits a hierarchy of *locally supported* functions, and therefore its solution reduces to a well-conditioned sparse linear system.

将曲面重构作为泊松问题来表述有许多优点。许多隐式曲面拟合方法将数据分割成区域进行局部拟合，然后使用混合函数进一步组合这些局部逼近。相比之下，泊松重构是一种一次性考虑所有数据的全局解决方案，不需要诉诸启发式分割或混合。因此，像径向基函数(RBF)方法，泊松重建创建非常光滑的表面，鲁棒地近似噪声数据。但是，理想的RBF是全局支持和非衰减的，泊松问题允许局部支持函数的层次结构，因此它的解简化为一个良好条件的稀疏线性系统。

Moreover, in many implicit fitting schemes, the value of the implicit function is constrained only near the sample points, and consequently the reconstruction may contain spurious surface sheets away from these samples. Typically this problem is attenuated by introducing auxiliary “off-surface” points (e.g. [CBC*∗*01, OBA*∗*03]). With Poisson surface reconstruction, such surface sheets seldom arise because the gradient of the implicit function is constrained at *all* spatial points. In particular it is constrained to zero away from the samples.

此外，在许多隐式拟合方案中，隐函数的值仅限制在样本点附近，因此重建可能包含远离这些样本的虚假表面片。通常，通过引入辅助的“非表面”点(例如[CBC * 01, OBA * 03])，这个问题会得到缓解。在泊松曲面重构中，由于隐函数的梯度约束在所有空间点上，这样的曲面片很少出现。特别地，它与样本的距离被限制为零。

Poisson systems are well known for their resilience in the presence of imperfect data. For instance, “gradient domain” manipulation algorithms (e.g. [FLW02]) intentionally modify the gradient data such that it no longer corresponds to any real potential field, and rely on a Poisson system to recover the globally best-fitting model.

泊松系统以其在不完全数据存在时的弹性而闻名。例如，“梯度域”操作算法(如[FLW02])有意地修改梯度数据，使其不再对应于任何真实的势场，并依靠泊松系统恢复全局最佳拟合模型。

There has been broad interdisciplinary research on solving Poisson problems and many efficient and robust methods have been developed. One particular aspect of our problem instance is that an accurate solution to the Poisson equation is only necessary near the reconstructed surface. This allows us to leverage adaptive Poisson solvers to develop a reconstruction algorithm whose spatial and temporal complexities are proportional to the size of the reconstructed surface.

在解决泊松问题方面已经有了广泛的跨学科研究，并发展了许多高效和稳健的方法。我们的问题实例的一个特殊方面是泊松方程的精确解只在重构曲面附近是必要的。这使得我们能够利用自适应泊松解算器来开发一种重建算法，其空间和时间的复杂性与重建曲面的大小成正比。



# 2. Related Work  

**Surface reconstruction** The reconstruction of surfaces from oriented points has a number of difficulties in practice. The point sampling is often nonuniform. The positions and normals are generally noisy due to sampling inaccuracy and scan misregistration. And, accessibility constraints during scanning may leave some surface regions devoid of data. Given these challenges, reconstruction methods attempt to infer the topology of the unknown surface, accurately fit (but not overfit) the noisy data, and fill holes reasonably.

 **曲面重建** 面向点的曲面重建在实际应用中存在许多困难。点采样通常是不均匀的。由于采样不准确和扫描错误配准，位置和法线通常是有噪声的。而且，扫描过程中的可访问性限制可能会使一些表面区域缺乏数据。鉴于这些挑战，重构方法试图推断未知表面的拓扑结构，准确拟合(但不过度拟合)噪声数据，并合理地填补漏洞。

Several approaches are based on combinatorial structures, such as Delaunay triangulations (e.g. [Boi84, KSO04]), alpha shapes [EM94, BBX95, BMR*∗*99]), or Voronoi diagrams [ABK98, ACK01]. These schemes typically create a triangle mesh that interpolates all or a most of the points. In the presence of noisy data, the resulting surface is often jagged, and is therefore smoothed (e.g. [KSO04]) or refit to the points (e.g. [BBX95]) in subsequent processing.

有几种方法是基于组合结构的，例如Delaunay三角剖分(例如[Boi84, KSO04])， alpha形状[EM94, BBX95, BMR * 99]，或Voronoi图[ABK98, ACK01]。这些方案通常创建一个三角形网格来插值所有或大部分的点。在有噪声数据的情况下，得到的表面往往是锯齿状的，因此在后续处理中需要进行平滑处理(如[KSO04])或对点进行修整(如[BBX95])。

Other schemes directly reconstruct an approximating surface, typically represented in implicit form. We can broadly classify these as either global or local approaches.

其他方案直接重建一个近似曲面，通常以隐式形式表示。我们可以大致将这些方法分为全局方法或局部方法。

Global fitting methods commonly define the implicit function as the sum of radial basis functions (RBFs) centered at the points (e.g. [Mur91, CBC*∗*01, TO02]). However, the ideal RBFs (polyharmonics) are globally supported and nondecaying, so the solution matrix is dense and ill-conditioned. Practical solutions on large datasets involve adaptive RBF reduction and the fast multipole method [CBC*∗*01].

全局拟合方法通常将隐函数定义为以点为中心的径向基函数之和(如[Mur91, CBC ∗ 01,TO02])。然而，理想的RBF(多谐波)是全局支持和不衰减的，因此解矩阵是密集和病态的。大数据集上的实际解决方案包括自适应RBF简化和快速多极方法[CBC ∗ 01]。

Local fitting methods consider subsets of nearby points at a time. A simple scheme is to estimate tangent planes and define the implicit function as the signed distance to the tangent plane of the closest point [HDD*∗*92]. Signed distance can also be accumulated into a volumetric grid [CL96]. For function continuity, the influence of several nearby points can be blended together, for instance using moving least squares [ABCO*∗*01,SOS04]. A different approach is to form point neighborhoods by adaptively subdividing space, for example with an adaptive octree. Blending is possible over an octree structure using a multilevel partition of unity, and the type of local implicit patch within each octree node can be selected heuristically [OBA*∗*03].

局部拟合方法每次考虑附近点的子集。一个简单的方案是估计切平面，并将隐函数定义为到最近点的切平面的符号距离[HDD * 92]。符号距离也可以累积成一个体积网格[CL96]。对于函数的连续性，可以将附近几个点的影响混合在一起，例如使用移动最小二乘[ABCO * 01,SOS04]。另一种方法是通过自适应细分空间形成点邻域，例如使用自适应八叉树。混合可以在一个八叉树结构上使用多级单位分区，并且可以启发式地选择每个八叉树节点中的局部隐式片段类型[OBA * 03]。

Our Poisson reconstruction combines benefits of both global and local fitting schemes. It is global and therefore does not involve heuristic decisions for forming local neighborhoods, selecting surface patch types, and choosing blend weights. Yet, the basis functions are associated with the ambient space rather than the data points, are locally supported, and have a simple hierarchical structure that results in a sparse, well-conditioned system.

我们的泊松重建结合了全局和局部拟合方案的优点。它是全局的，因此不涉及形成局部邻域、选择表面斑块类型和选择混合权值的启发式决策。然而，基函数是与环境空间而不是数据点相关联的，是本地支持的，并且具有一个简单的层次结构，从而形成一个稀疏的、条件良好的系统。

Our approach of solving an indicator function is similar to the Fourier-based reconstruction scheme of Kazhdan [Kaz05]. In fact, we show in Appendix A that our basic Poisson formulation is mathematically equivalent. Indeed, the Fast Fourier Transform (FFT) is a common technique for solving *dense*, *periodic* Poisson systems. However, the FFT requires *O*(*r*3 log*r*) time and *O*(*r*3) space where *r* is the 3D grid resolution, quickly becoming prohibitive for fine resolutions. In contrast, the Poisson system allows adaptive discretization, and thus yields a scalable solution.

我们求解指标函数的方法类似于Kazhdan [Kaz05]的基于傅里叶的重构方案。事实上，我们在附录A中表明，我们的基本泊松公式在数学上是等价的。事实上，快速傅里叶变换(FFT)是求解 *密集* 、 *周期* 泊松系统的常用技术。然而，FFT需要 *O*(*r*3 log*r*) 时间和 *O*(*r*3) 空间，其中 *r* 是3D网格分辨率，很快就无法实现高分辨率。相反，泊松系统允许自适应离散化，从而产生可扩展的解决方案。

**Poisson problems** The Poisson equation arises in numerous applications areas. For instance, in computer graphics it is used for tone mapping of high dynamic range images [FLW02], seamless editing of image regions [PGB03], fluid mechanics [LGF04], and mesh editing [YZX*∗*04]. Multigrid Poisson solutions have even been adapted for efficient GPU computation [BFGS03, GWL*∗*03].

**泊松问题** 泊松方程出现在许多应用领域。例如，在计算机图形学中，它用于高动态范围图像的色调映射[FLW02]、图像区域的无缝编辑[PGB03]、流体力学[LGF04]和网格编辑[YZX * 04]。多重网格泊松解甚至被用于高效的GPU计算[BFGS03, GWL * 03]。

The Poisson equation is also used in heat transfer and diffusion problems. Interestingly, Davis et al [DMGL02] use diffusion to fill holes in reconstructed surfaces. Given boundary conditions in the form of a clamped signed distance function $d$ , their diffusion approach essentially solves the homogeneous Poisson equation $\vartriangle d =0$ to create an implicit surface spanning the boundaries. They use a local iterative solution rather than a global multiscale Poisson system.

泊松方程也用于传热和扩散问题。有趣的是，Davis等[DMGL02]利用扩散来填充重构表面的孔洞。给定一个固定的符号距离函数 $d$ 形式的边界条件，他们的扩散方法本质上是求解齐次泊松方程  $\vartriangle d =0$，以创建跨越边界的隐式曲面。它们使用局部迭代解，而不是全局多尺度泊松系统。

Nehab et al [NRDR05] use a Poisson system to fit a 2.5D height field to sampled positions and normals. Their approach fits a given parametric surface and is well-suited to the reconstruction of surfaces from individual scans. However, in the case that the samples are obtained from the union of multiple scans, their approach cannot be directly applied to obtain a connected, watertight surface.

Nehab等人[NRDR05]使用泊松系统将2.5D高度场与采样位置和法线拟合。他们的方法适合一个给定的参数表面，并非常适合从个别扫描重建表面。然而，如果样品是通过多次扫描的联合获得的，他们的方法不能直接应用于获得连接的、严密的表面。



# 3. Our Poisson reconstruction approach

The input data $S$ is a set of samples $s \in S$ , each consisting of a point $s.p$ and an inward-facing normal $s.\vec{N}$ , assumed to lie on or near the surface $\partial M$ of an unknown model $M$ . Our goal is to reconstruct a watertight, triangulated approximation to the surface by approximating the indicator function of the model and extracting the isosurface, as illustrated in Figure 2.

输入数据 $S$ 是一组以 $s \in S$  为单位的样本，每个样本由一个点 $s.p$ 和一个向内的法线 $s.\vec{N}$ ，假定位于和接近一个未知的模型 $M$ 的表面 $\partial M$ 。我们的目标是通过逼近模型的指示函数并提取等值面来重建一个严密的、三角逼近的表面，如图2所示。

![image-20220810125311552](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208101253635.png)

> 图2:“犰狳人”模型(左)的扫描点，我们的泊松表面重建(右)，以及指示器函数的可视化(中)沿着一个平面通过3D体。

The key challenge is to accurately compute the indicator function from the samples. In this section, we derive a relationship between the gradient of the indicator function and an integral of the surface normal field. We then approximate this surface integral by a summation over the given oriented point samples. Finally, we reconstruct the indicator function from this gradient field as a Poisson problem.

关键的挑战是如何从样本中准确地计算指标函数。在本节中，我们推导出指示函数的梯度与表面法向场的积分之间的关系。然后，我们通过对给定的定向点样本求和来近似这个曲面积分。最后，我们将这个梯度场重构为一个泊松问题。

**Defining the gradient field** Because the indicator function is a piecewise constant function, explicit computation of its gradient field would result in a vector field with unbounded values at the surface boundary. To avoid this, we convolve the indicator function with a smoothing filter and consider the gradient field of the smoothed function. The following lemma formalizes the relationship between the gradient of the smoothed indicator function and the surface normal field.

**定义梯度场** 由于指示函数是分段常数函数，显式计算其梯度场将得到一个在曲面边界上具有无界值的向量场。为了避免这种情况，我们将指标函数与平滑滤波器进行卷积，并考虑平滑函数的梯度场。下面的引理形式化了平滑指示函数的梯度和表面法向量场之间的关系。

**Lemma**: Given a solid $M$ with boundary $\partial M$ , let $\mathcal{X} _M$ denote the indicator function of $M$ , $\vec{N}_{\partial M}(p)$ be the inward surface normal at $p \in \partial M$ , $\tilde{F}(q)$ be a smoothing filter, and $\tilde{F}_p(q) = \tilde{F}(q-p)$ its translation to the point $p$ . The gradient of the smoothed indicator function is equal to the vector field obtained by smoothing the surface normal field:

**引理** 给定一个具有边界 $\partial M$ 的实体 $M$ ，让 $\mathcal{X} _M$ 表示 $M$ 的指示函数， $\vec{N}_{\partial M}(p)$ 是在 $\partial M$ 中 $p \in \partial M$ 的内表面法线， $\tilde{F}(q)$ 是一个平滑滤波器， $\tilde{F}_p(q) = \tilde{F}(q-p)$ 其转换到点 $p$ 。平滑指示函数的梯度等于对表面法向场进行平滑得到的向量场:
$$
\nabla(\mathcal{X}_M*\tilde{F})(q_0) = \int_{\partial M} \tilde{F}_p(q_0)\vec{N}_{\partial M}(p)dp. \tag{1}
$$
**Proof**: To prove this, we show equality for each of the components of the vector field. Computing the partial derivative of the smoothed indicator function with respect to *x*, we get:

**证明** :为了证明这个，我们证明向量场的每个分量是相等的。计算平滑指标函数对 $x$ 的偏导数，得到:
$$
\begin{aligned}
\frac{\partial}{\partial x}\Bigg|_{q_0} (\mathcal{X}_M*\tilde{F}) &= \frac{\partial}{\partial x}\Bigg|_{q=q_0} \int_M \tilde{F}(q-p)dp\\
&=\int_M\Bigg(-\frac{\partial}{\partial x} \tilde{F}(q_0-p)  \Bigg)dp\\
&= -\int_M \nabla \cdot (\tilde{F}(q_0-p),0,0)dp \\
&=\int_{\partial M} \Big<(\tilde{F}_p(q_0),0,0), \vec{N}_{\partial M}(p)  \Big> dp.
\end{aligned}
$$
(The first equality follows from the fact that $\mathcal{X}_M$ is equal to zero outside of $M$ and one inside. The second follows from the fact that $(\partial/\partial q)\tilde{F}(q-p)=-(\partial/\partial p)\tilde{F}(q-p)$ . The last follows from the Divergence Theorem.)

(第一个等式源于 $\mathcal{X}_M$ 在 $M$ 外等于0，在 $M$ 内等于1。第二个是由 $(\partial/\partial q)\tilde{F}(q-p)=-(\partial/\partial p)\tilde{F}(q-p)$ 。最后一个来自散度定理。)

A similar argument shows that the *y*-, and *z*-components of the two sides are equal, thereby completing the proof.

类似的论证表明，两边的y分量和z分量是相等的，从而完成了证明。

**Approximating the gradient field** Of course, we cannot evaluate the surface integral since we do not yet know the surface geometry. However, the input set of oriented points provides precisely enough information to approximate the integral with a discrete summation. Specifically, using the point set $S$ to partition $\partial M$ into distinct patches $\mathscr{P}_s \subset \partial M$ , we can approximate the integral over a patch $\mathscr{P}_s$ by the value at point sample $s.p$ , scaled by the area of the patch:

当然，我们不能计算曲面积分，因为我们还不知道曲面的几何形状。然而，定向点的输入集提供了足够精确的信息来用离散求和近似积分。具体地说，使用点集 $S$ 将 $\partial M$ 划分为不同的片段 $\mathscr{P}_s \subset M$ ，我们可以用点样本 $s.p$  的值来近似一个片段 $\mathscr{P}_s$ 上的积分，按片段的面积缩放:
$$
\begin{aligned}
\nabla(\mathcal{X}_M * \tilde{F})(q) &= \sum_{s\in S} \int_{\mathscr{P}_s} \tilde{F}_p(q)\vec{N}_{\partial M}(p)dp \\
& \approx \sum_{s\in S}|\mathscr{P}_s|\tilde{F}_{s.p}(q)s.\vec{N} \equiv \vec{V}(q). 
\end{aligned}\tag{2}
$$
It should be noted that though Equation 1 is true for any smoothing filter $\tilde{F}$ , in practice, care must be taken in choosing the filter. In particular, we would like the filter to satisfy two conditions. On the one hand, it should be sufficiently narrow so that we do not over-smooth the data. And on the other hand, it should be wide enough so that the integral over $\mathscr{P}_s$ is well approximated by the value at $s.p$ scaled by the patch area. A good choice of filter that balances these two requirements is a Gaussian whose variance is on the order of the sampling resolution.

需要注意的是，虽然等式1对任何平滑滤波器 $\tilde{F}$ 都成立，但实际上，在选择滤波器时必须小心。特别地，我们希望过滤器满足两个条件。一方面，它应该足够窄，这样我们就不会过度平滑数据。另一方面，它应该足够宽，以便对 $\mathscr{P}_s$ 的积分可以很好地近似于按片段面积缩放的 $s.p$ 的值。平衡这两种要求的滤波器的一个很好的选择是一个高斯滤波器，其方差与采样分辨率有关。

**Solving the Poisson problem** Having formed a vector field $\vec{V}$ , we want to solve for the function $\tilde{\mathcal{X}}$ such that $\nabla \tilde{\mathcal{X}}=\vec{V}$ . However, $\vec{V}$ is generally not integrable (i.e. it is not curlfree), so an exact solution does not generally exist. To find the best least-squares approximate solution, we apply the divergence operator to form the Poisson equation

已经形成了一个矢量域 $\vec{V}$ ，我们想要解决函数 $\tilde{\mathcal{X}}$ ，这样 $\nabla \tilde{\mathcal{X}}=\vec{V}$ 。然而， $\vec{V}$ 通常是不可积的(即它不是无卷曲的)，因此一般不存在精确解。为了找到最佳的最小二乘近似解，我们应用散度算子形成泊松方程
$$
\nabla \tilde{\mathcal{X}} = \vartriangle \cdot \vec{V}
$$
In the next section, we describe our implementation of these steps in more detail.  

在下一节中，我们将更详细地描述这些步骤的实现。



# 4.Implementation（实现）

We first present our reconstruction algorithm under the assumption that the point samples are uniformly distributed over the model surface. We define a space of functions with high resolution near the surface of the model and coarser resolution away from it, express the vector field $\vec{V}$ as a linear sum of functions in this space, set up and solve the Poisson equation, and extract an isosurface of the resulting indicator function. We then extend our algorithm to address the case of non-uniformly sampled points.

在假设点样本均匀分布于模型表面的前提下，提出了重构算法。我们在模型表面附近定义了一个高分辨率和较粗分辨率的函数空间，将该空间中的向量场 $\vec{V}$ 表示为函数的线性和，建立并求解泊松方程，并提取出结果指示函数的等值面。然后我们扩展我们的算法，以解决非均匀采样点的情况。















