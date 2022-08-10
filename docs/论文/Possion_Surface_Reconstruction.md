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

面向点曲面重建在实际应用中存在许多困难。点采样通常是不均匀的。由于采样不准确和扫描错误配准，位置和法线通常是有噪声的。而且，扫描过程中的可访问性限制可能会使一些表面区域缺乏数据。鉴于这些挑战，重构方法试图推断未知表面的拓扑结构，准确拟合(但不过度拟合)噪声数据，并合理地填补漏洞。

Several approaches are based on combinatorial structures, such as Delaunay triangulations (e.g. [Boi84, KSO04]), alpha shapes [EM94, BBX95, BMR*∗*99]), or Voronoi diagrams [ABK98, ACK01]. These schemes typically create a triangle mesh that interpolates all or a most of the points. In the presence of noisy data, the resulting surface is often jagged, and is therefore smoothed (e.g. [KSO04]) or refit to the points (e.g. [BBX95]) in subsequent processing.

有几种方法是基于组合结构的，例如Delaunay三角剖分(例如[Boi84, KSO04])， alpha形状[EM94, BBX95, BMR * 99]，或Voronoi图[ABK98, ACK01]。这些方案通常创建一个三角形网格来插值所有或大部分的点。在有噪声数据的情况下，得到的表面往往是锯齿状的，因此在后续处理中需要进行平滑处理(如[KSO04])或对点进行修整(如[BBX95])。

Other schemes directly reconstruct an approximating surface, typically represented in implicit form. We can broadly classify these as either global or local approaches.

其他方案直接重建一个近似曲面，通常以隐式形式表示。我们可以大致将这些方法分为全局方法或局部方法。

Global fitting methods commonly define the implicit function as the sum of radial basis functions (RBFs) centered at the points (e.g. [Mur91, CBC*∗*01, TO02]). However, the ideal RBFs (polyharmonics) are globally supported and nondecaying, so the solution matrix is dense and ill-conditioned. Practical solutions on large datasets involve adaptive RBF reduction and the fast multipole method [CBC*∗*01].

全局拟合方法通常将隐函数定义为以点为中心的径向基函数之和(如[Mur91, CBC ∗ 01,TO02])。然而，理想的RBF(多谐波)是全局支持和不衰减的，因此解矩阵是密集和病态的。大数据集上的实际解决方案包括自适应RBF简化和快速多极方法[CBC ∗ 01]。

Local fitting methods consider subsets of nearby points at a time. A simple scheme is to estimate tangent planes and define the implicit function as the signed distance to the tangent plane of the closest point [HDD*∗*92]. Signed distance can also be accumulated into a volumetric grid [CL96]. For function continuity, the influence of several nearby points can be blended together, for instance using moving least squares [ABCO*∗*01,SOS04]. A different approach is to form point neighborhoods by adaptively subdividing space, for example with an adaptive octree. Blending is possible over an octree structure using a multilevel partition of unity, and the type of local implicit patch within each octree node can be selected heuristically [OBA*∗*03].

局部拟合方法每次考虑附近点的子集。一个简单的方案是估计切平面，并将隐函数定义为到最近点的切平面的符号距离[HDD * 92]。符号距离也可以累积成一个体积网格[CL96]。对于函数的连续性，可以将附近几个点的影响混合在一起，例如使用移动最小二乘[ABCO * 01,SOS04]。另一种方法是通过自适应细分空间形成点邻域，例如使用自适应八叉树。混合可以在一个八叉树结构上使用多级单位分区，并且可以启发式地选择每个八叉树节点中的局部隐式片段类型[OBA * 03]。





