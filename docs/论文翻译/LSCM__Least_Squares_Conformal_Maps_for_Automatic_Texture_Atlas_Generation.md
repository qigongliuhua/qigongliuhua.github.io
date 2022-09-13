> **Least Squares Conformal Maps  for Automatic Texture Atlas Generation  **



# 摘要

A Texture Atlas is an efficient color representation for 3D Paint Systems. The model to be textured is decomposed into charts homeomorphic to discs, each chart is parameterized, and the unfolded charts are packed in texture space. Existing texture atlas methods for triangulated surfaces suffer from several limitations, requiring them to generate a large number of small charts with simple borders. The discontinuities between the charts cause artifacts, and make it difficult to paint large areas with regular patterns.

纹理图集是3D绘图系统的有效颜色表示。将需要纹理的模型分解为与圆盘同胚的图表，对每个图表进行参数化，并将展开的图表打包到纹理空间中。现有的三角曲面纹理图集方法存在一些局限性，需要生成大量边框简单的小图表。图表之间的不连续性会导致伪影（鬼影），这使得用规则模式绘制大面积区域变得困难。

In this paper, our main contribution is a new quasi-conformal parameterization method, based on a least-squares approximation of the Cauchy-Riemann equations. The so-defined objective function minimizes angle deformations, and we prove the following properties: the minimum is unique, independent of a similarity in texture space, independent of the resolution of the mesh and cannot generate triangle flips. The function is numerically well behaved and can therefore be very efficiently minimized. Our approach is robust, and can parameterize large charts with complex borders.

本文的主要贡献是基于柯西-黎曼方程的最小二乘近似，提出了一种新的准共形参数化方法。这样定义的目标函数最小化角度变形，我们证明了以下性质:最小值是唯一的，与纹理空间的相似性无关，与网格的分辨率无关，不能生成三角形翻转。该函数在数值上表现良好，因此可以非常有效地最小化。我们的方法是稳健的，可以参数化具有复杂边界的大型图表。

We also introduce segmentation methods to decompose the model into charts with natural shapes, and a new packing algorithm to gather them in texture space. We demonstrate our approach applied to paint both scanned and modeled data sets.

我们还引入了分割方法将模型分解为具有自然形状的图表，以及一种新的打包算法将它们聚集在纹理空间。我们将演示如何绘制扫描数据集和建模数据集。

> **CR Categories:** I.3.3 [Computer Graphics] Picture/Image Generation; I.3.5 [Computer Graphics]: Three-Dimensional Graphics and Realism—Color, shading, shadowing and texture; I.4.3 [Image processing]: Enhancement—Geometric Correction, Texture

> **Keywords:** Texture Mapping, Paint Systems, Polygonal Modeling



# 1 引言

A 3D paint system makes it possible to enhance the visual appearance of a 3D model by interactively adding details to it (colors, bump maps . . . ). If the discretization of the surface is fine enough, it is possible to directly paint its vertices [1]. However, in most cases, the desired precision for the colors is finer than the geometric details of the model. Assuming that the surface to be painted is provided with a parameterization, it is possible to use texture mapping to store colors in parameter space [9]. Parametric surfaces (such as NURBS) have a natural parameterization. For other representations, such as polygonal surfaces, finding a parameterization is non-trivial. To decorate polygonal models with regular patterns, the *lapped textures* approach [26] can be applied: local overlapping parameterizations are used to repeatedly map a small texture swatch onto a model.

3D绘图系统可以通过交互添加细节(颜色、凹凸贴图……)来增强3D模型的视觉外观。如果表面的离散化足够精细，就可以直接绘制它的顶点[1]。然而，在大多数情况下，所需的颜色精度要比模型的几何细节更精确。假设要绘制的表面具有参数化，则可以使用纹理映射将颜色存储在参数空间[9]中。参数化曲面(如NURBS)具有自然参数化。对于其他表示，如多边形曲面，寻找参数化是很重要的。为了用规则的模式粉刷多边形模型，可以应用 *重叠纹理* 方法[26]:局部重叠参数被用来重复映射一个小的纹理样本到一个模型上。

A texture atlas is a more general representation (see, e.g., [13, 20, 23]). The model to be textured is partitioned into a set of parts homeomorphic to discs, referred to as *charts*, and each of them is provided with a parameterization. A texture atlas can be easily represented by standard file formats and displayed using standard texture mapping hardware. When used in a 3D paint system, a texture atlas should meet the following requirements:

纹理图集是一种更一般的表示(如[13,20,23])。被纹理化的模型被划分为一组与圆盘同胚的部分，称为图表，每个部分都有一个参数化。一个纹理图集可以很容易地用标准文件格式表示，并使用标准纹理映射硬件显示。在3D绘制系统中使用时，纹理图集应满足以下要求:

+ the chart boundaries should be chosen to minimize texture artifacts,
+ the sampling of texture space should be as uniform as possible,
+ the atlas should make an optimal use of texture space.
+ 图表边界的选择应该尽量减少纹理的影响，
+ 纹理空间的采样应尽可能均匀，
+ 图集应该充分利用纹理空间。

The generation of a texture atlas can be decomposed into the following steps:

纹理图集的生成可以分解为以下步骤:

1. **Segmentation:** The model is partitioned into a set of charts.
2. **Parameterization:** Each chart is ‘unfolded’, i.e. put in correspondence with a subset of $\Reals^2$.
3. **Packing:** The charts are gathered in texture space.

1.  **分割:** 将模型划分为一组图表。

2.  **参数化:** 每个图表都是“展开的”，即与 $\Reals^2$ 的子集对应。
3.  **包装:** 图表聚集在纹理空间中。

The remainder of this section presents the existing methods for these three steps, and their limitations with respect to the requirements mentioned above. We then introduce a new texture atlas generation method, meeting these requirements by creating charts with natural shapes, thus reducing texture artifacts.

本节的其余部分将介绍这三个步骤的现有方法，以及它们对上述需求的限制。然后我们引入了一种新的纹理图集生成方法，通过创建具有自然形状的图表来满足这些需求，从而减少了纹理伪影（鬼影）。

## 1.1 先前的工作

**Segmentation into charts.** In [14] and [23], the model is interactively partitioned by the user. To perform automatic segmentation, Maillot *et al.* [20] group the facets by their normals. Several multiresolution methods [7, 16] decompose the model into charts corresponding to the simplices of the base complex. In [27], Sander *et al.* use a region-growing approach to segmentation, merging charts according to both planarity and compactness criteria. All these approaches are designed to produce charts that can be treated by existing parameterization methods, which are limited to charts with convex borders. For this reason, a large number of charts is generated, which introduces many discontinuities when constructing a texture atlas.

**分割成图表。** 在[14]和[23]中，模型由用户交互分区。为了执行自动分割，$Maillot$ 等人[20]根据 facet 的法线对它们进行分组。几种多分辨率方法[7,16]将模型分解为与基本复合体的单体相对应的图表。在[27]中，$Sander$ 等人使用区域增长的方法进行分割，根据平面性和紧凑性标准合并图表。所有这些方法都是为了生成可被现有参数化方法处理的图表，而现有参数化方法仅限于具有凸边界的图表。因此，会产生大量的图表，在构造纹理图集时引入了许多不连续。



**Chart parameterization.** Discrete Harmonic Map, described by Eck *et al.* [4], are the most widely used. They are approximations of Continuous Harmonic Maps [5], minimizing a *metric dispersion* criterion. Pinkal and Polthier [24] have shown the link between this criterion and another one named *conformality*, and have expressed both in terms of *Dirichlet energy*. Haker *et al.* [8] describe a similar method in the specific case of a surface triangulation homeomorphic to a sphere.

**图参数化。** 由 $Eck$ 等人[4]描述的离散谐波映射是应用最广泛的。它们是连续谐波映射[5]的近似，最小化度量分散准则。 $Pinkal$ 和 $Polthier$ [24]已经证明了这个准则和另一个名为共形性之间的联系，并以 “狄利克雷能量“ 来表示它们。 $Haker$ 等人[8]描述了球面同胚表面三角剖分的一种类似方法。

The theory on graph embedding has been studied by Tutte [30], where *Barycentric Maps* are introduced. The bijectivity of the sodefined parameterization is mathematically guaranteed. Floater [6] proposes specific weights improving the quality of the mapping, in terms of area deformations and conformality. In [18], a method is proposed to take additional constraints into account.

 $Tutte$ [30]研究了图嵌入的理论，其中引入了重心图。在数学上是可以保证这样定义的参数化的双射性。 $$Floater$$ [6]提出了特定的权重，从面积变形和共形两个方面提高了映射的质量。在[18]中，提出了一种考虑额外约束的方法。

In all the methods mentioned above, since conformality is expressed as an indirect coupling between the parameters, boundary conditions are required, i.e. boundary nodes need to be fixed on a convex border in parameter space. Other expressions of conformality, such as the non-linear MIPS method [10], make it possible to overcome this problem, and let the boundary nodes be free to move. However, this latter method requires a time-consuming non-linear optimization, and may get stuck in a local minima of the non-linear function. In [12], Hurdal *et al.* propose a method based on *circle packings*, which are certain configurations of circles with specified pattern of tangencies known to provide a way to approximate a conformal mapping. Building circle packings is however quite expensive. The approach proposed in [28] consists in solving for the angles in parameter space. It results in a highly constrained optimization problem. Other methods [17, 25, 31] can also extrapolate the border, but do not guarantee the absence of triangle flips and require interaction with the user. We introduce here a conformal mapping method, offering more guarantees, efficiency and robustness than those approaches.

在上述所有方法中，由于共形性都表示为参数之间的间接耦合，因此需要有边界条件，即边界节点需要固定在参数空间的凸边界上。其他的共形表达式，如非线性 **MIPS** 方法[10]，使克服这一问题成为可能，并使边界节点自由移动。然而，后一种方法需要耗时的非线性优化，并可能陷入非线性函数的局部极小值。在[12]中，**Hurdal** 等人提出了一种基于圆填充的方法，它是具有特定切线模式的圆的某些配置，提供了一种近似保角映射的方法。然而，建造圆形包装是相当昂贵的。[28]中提出的方法是在参数空间中求解角度。它导致了一个高度约束的优化问题。其他方法[17,25,31]也可以外推边界，但不能保证没有三角翻转，需要与用户交互。本文介绍了一种保角映射方法，该方法比上述方法具有更高的保密性、效率和鲁棒性。

In the case of texture mapping, not only the bijectivity of the parameterization should be ensured, but also its ability to make an optimum use of texture memory, and to accurately represent a signal stored in texture space. Sander *et. al.* [27] describe an approach to minimize both a *texture stretch* criterion, and texture deviation between level of details. Since their approach is independent from the initial parameterization method, it can be applied to optimize the sampling of the parameterizations constructed by our method.

在纹理映射的情况下，不仅要保证参数化的双射性，还要保证参数化能够充分利用纹理内存，准确地表示存储在纹理空间中的信号。 $Sander$ 等人[27]描述了一种最小化纹理拉伸准则和细节级别之间纹理偏差的方法。由于它们的方法独立于初始参数化方法，因此可以用于优化由我们的方法构造的参数化的抽样。



**Charts packing in texture space.** Finding the optimal packing of the charts in texture space is known as the *bin packing* problem. It has been studied by several authors, such as Milenkovic (see, e.g., [21]), but the resulting algorithms take a huge amount of time since the problem is NP-complete. To speed up these computations, several heuristics have been proposed in the computer graphics community. In the case of individual triangles, such a method is described by several authors (see, e.g., [3]). In the general case of charts, Sander *et al.* [27] propose an approach to pack the minimal area bounding rectangles of the charts. In our case, since the charts can have arbitrarily shaped borders, the bounding rectangle can be far away from the boundary of the charts. Therefore, a lot of texture space can be wasted. For this reason, we propose a more accurate packing algorithm that can handle the complex charts created by our segmentation and parameterization methods.

**图表包装在纹理空间。**在纹理空间中找到图表的最佳包装被称为 *bin包装* 问题。它已经被几位作者研究过了，比如 $Milenkovic$ (参见[21])，但是由于问题是NP完全的，得到的算法需要大量的时间。为了加快计算速度，计算机图形界提出了几种启发式算法。在单个三角形的情况下，这种方法由几个作者描述(参见，例如[3])。在图表的一般情况下，$Sander$ 等人[27]提出了一种对图表的最小面积包围矩形进行打包的方法。在我们的示例中，由于图表可以具有任意形状的边框，所以边界矩形可以远离图表的边界。因此，大量的纹理空间会被浪费掉。为此，我们提出了一种更精确的打包算法，可以处理由我们的分割和参数化方法创建的复杂图表。



## 1.2 概述

The paper is organized as follows. Since it is our main contribution, we will start by introducing Least Squares Conformal Maps (LSCMs), a new optimization-based parameterization method with the following properties (see Section 2 and Figure 1):

本文的组织结构如下。由于这是我们的主要贡献，我们将首先介绍最小二乘共形映射( **LSCMs** )，这是一种新的基于优化的参数化方法，具有以下特性(参见第2节和图1):

+ Our criterion **minimizes angle deformations and non-uniform scalings**. It can be efficiently minimized by classical NA methods, and does not require a complex algorithm such as the ones used in [12] and in [28].
+ We prove the **existence and uniqueness of the minimum** of this criterion. Therefore, the solver cannot get stuck in a local minimum, in contrast with non-linear methods [10, 25, 27, 31] where this property is not guaranteed.
+ The borders of the charts do not need to be fixed, as with most of the existing methods [4, 6, 18]. Therefore, **large charts with arbitrarily shaped borders** can be parameterized.
+ We prove that the orientation of the triangles is preserved, which means that **no triangle flip can occur**. However, as in [28], overlaps may appear, when the boundary of the surface self-intersects in texture space. Such configurations are automatically detected, and the concerned charts are subdivided. This problem was seldom encountered in our experiments (note that as with classical methods [4, 6], if all the border nodes are fixed on a convex polygon, no overlap can occur).
+ We prove that the result is **independent of the resolution of the mesh**. This type of property may be usefull to reduce texture deviation when parameterizing different level of details of the same object.

+ 我们的准则 **最小化角度变形和非均匀缩放** 。该算法不需要[12]和[28]算法那样复杂的算法，可以用经典的NA方法有效地将其最小化。
+ 我们证明了该准则的 **最小值的存在唯一性** 。因此，解算器不会陷入局部最小值，与非线性方法[10,25,27,31]相比，非线性方法不能保证此属性。
+ 图表的边界不需要固定，与大多数现有的方法[4,6,18]。因此，**具有任意形状边界的大图表**可以被参数化。
+ 我们证明了三角形的方向是保持不变的，这意味着**不会发生三角形翻转**。然而，在[28]中，当表面边界在纹理空间中自交时，可能会出现重叠。这样的配置是自动检测的，相关的图表被细分。在我们的实验中很少遇到这个问题(注意，与经典方法[4,6]一样，如果所有边界节点都固定在一个凸多边形上，就不会发生重叠)。
+ 我们证明了结果**与网格的分辨率无关**。当对同一对象的不同细节级别进行参数化时，这种类型的属性可能有助于减少纹理偏差。

![image-20220720144025619](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207201440683.png)

> *图1:扫描的马的身体是对方法鲁棒性的测试用例;这是一个由72,438个三角形组成的非常大的图表，有着复杂的边界。A:得到的等参数曲线; B:对应的展开表面，边界已经自动外推; C:这些切口使表面相当于一个圆盘; D:参数化是稳健的，不受圈内大三角形的影响(扫描过程中出现的阴影区域造成的)。*



In Section 3, we present a new segmentation method to decompose the model into charts. Thanks to the additional flexibility offered by LSCMs, it is possible to create large charts corresponding to meaningful geometric entities, such as biological features of characters and animals. The required number of charts is dramatically reduced, together with the artifacts caused by the discontinuities between the charts. Moreover, these large charts facilitate the use of regular patterns in a 3D paint system.

在第3节中，我们提出了一种新的分割方法，将模型分解为图表。由于 **LSCMs** 提供了额外的灵活性，可以创建与有意义的几何实体(如人物和动物的生物特征)对应的大型图表。所需的图表数量大大减少，同时也减少了图表之间不连续性造成的伪影（鬼影）数量。此外，这些大图表便于在3D绘图系统中使用规则模式。

Section 4 presents our method to pack the charts in texture space. Since our segmentation method can create charts with complex borders, we pack the charts more accurately than with bounding rectangles, as in previous approaches. Our method is inspired by the strategy used by a ‘Tetris’ player. The paper concludes with some results, on both scanned and modeled meshes.

第4节介绍了我们在纹理空间中打包图表的方法。由于我们的分割方法可以创建具有复杂边界的图表，所以与前面的方法相比，我们可以更准确地打包图表。我们的方法是受到《俄罗斯方块》玩家所使用的策略的启发。最后给出了扫描网格和建模网格的一些结果。



# 2 LEAST SQUARES CONFORMAL MAPS  

In this section, we focus on the problem of parameterizing a chart homeomorphic to a disc. It will then be shown how to decompose the model into a set of charts, and how to pack these charts in texture space.

在本节中，我们着重于将圆盘同胚图表参数化的问题。然后将展示如何将模型分解为一组图表，以及如何将这些图表打包到纹理空间中。

## 2.1 符号

+ scalars are denoted by normal characters $x,y,u,v$ ,
+ vectors are denoted by bold characters $\mathbf{x}=(x,y)$ ,
+ complex numbers are denoted by capitals $U=(u+iv)$ ,
+ vectors of complex numbers are denoted by bold capitals $\mathbf{U}$ ,
+ maps and matrices are denoted by cursive fonts $\mathcal{U,X}$ .

+ 标量用普通字符 $x,y,u,v$ ，
+ 向量用粗体表示 $\mathbf{x}=(x,y)$ ，
+ 复数用大写表示 $U=(u +iv)$ ，
+ 复数向量用粗体大写 $\mathbf{U}$ 表示，
+ 映射和矩阵用草书字体 $\mathcal{U,X}$ 表示。



## 2.2 Conformal Maps 共形映射

In this section, we quickly introduce the notion of conformal map. We will present further a new way to approximate the conformality criterion and the mathematical properties of this approximation.

在本节中，我们快速介绍共形映射的概念。我们将进一步提出一种新的方法来近似共形准则和这种近似的数学性质。

![image-20220720144432984](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207201444031.png)

> 图2:在一个共形映射中，与iso-u和iso-v曲线的切向量是正交的，并且具有相同的长度。

As shown in Figure 2, an application $\mathcal{X}$ mapping $a(u,v)$ domain to a surface is said to be conformal if for each $(u,v)$ , the tangent vectors to the iso-$u$ and iso-$v$ curves passing through  are $\mathcal{X}(u,v)$ orthogonal and have the same norm, which can be written as:

如图2所示，一个 $\mathcal{X}$ 应用程序将 $a(u,v)$ 域映射到一个曲面，如果对于每一个 $(u,v)$ ，过 $\mathcal{X}(u,v)$ 的iso-$u$ 和iso-$v$ 曲线上的两个切向量是正交的，并且具有相同的模，则被认为是共形的，可以写成:
$$
N(u,v) \quad \times \quad \frac{\partial\mathcal{X}}{\partial u}(u,v) \quad = \quad \frac{\partial\mathcal{X}}{\partial v}(u,v), \tag{1}
$$
where $N(u,v)$ denotes the unit normal to the surface. In other words, a conformal map is *locally isotropic*, i.e. maps an elementary circle of the $(u,v)$ domain to an elementary circle of the surface.

其中 $N(u,v)$ 表示垂直于曲面的单位。换句话说，一个共形映射是*局部各向同性*，即映射$(u,v)$域的基本圆到曲面的基本圆。

It is possible to rewrite Equation 1 using differential operators, such as Laplace-Beltrami, as done in [24] and in [8], which results in the well known *cotangent* weighting coefficients (see e.g. [4]). The $(u,v)$ parameters are then found to be the solution of two separate linear systems, one for $u$ and one for $v$ . The relation between $u$ and $v$ is **indirectly** taken into account by the right hand sides of the two systems. For this reason, this type of method requires the border to be fixed on a convex polygon. The MIPS method [10] does not have this restriction, and expresses conformality as a relation linking the coefficients of the metric tensor. However, the resulting equations are non-linear. Another approach has been described in [28], based on the remark that the criterion defining a conformal mapping should be independent of a translation, rotation and scaling in parameter space (i.e. a *similarity*). The unknowns are the angles at the corners of the triangles. This requires a timeconsuming **constrained** optimization method.

可以使用微分算子重写方程1，如在[24]和[8]中所做的**Laplace-Beltrami**，这将得到众所周知的余切加权系数(参见[4])。然后发现 $(u,v)$ 参数是两个独立线性系统的解，一个为 $u$ ，一个为 $v$ 。$u$ 和 $v$ 之间的关系被两个系统的右手准则间接地考虑进去。因此，这种方法要求边界固定在凸多边形上。**MIPS**方法[10]不受此限制，将共形性表示为度量张量系数之间的关系。然而，得到的方程是非线性的。[28]中描述了另一种方法，基于定义共形映射的准则应该独立于参数空间中的平移、旋转和缩放(即*相似性*)。未知数是三角形角上的角。这需要一种耗时**受限**的优化方法。

Rather than discretizing the Laplace operator at the vertices of the triangulation, we instead take the dual path of considering the conformality condition on the triangles of the surface. Using the fact that a similarity can be represented by the product of complex numbers, we show how to turn the conformality problem into an **unconstrained** quadratic minimization problem. The $u$ and $v$ parameters are linked by a single global equation. This **direct** coupling of the $u$ and $v$ parameters makes it possible to efficiently parameterize large charts with complex borders, as shown in Figure 1. In this example, the cuts have been done manually (Figure 1-C), to create a large test case for the robustness of the method. (It will be shown in Section 3 how to automatically cut a model into charts homeomorphic to discs.)

我们不把拉普拉斯算子离散化在三角剖分的顶点上，而是在曲面的三角形上考虑共形条件。利用相似度可以由复数乘积表示的事实，我们展示了如何将保形问题转化为一个无约束的二次极小化问题。$u$ 和 $v$ 参数通过一个全局方程联系在一起。$u$ 和 $v$ 参数的这种直接耦合使得有效地参数化具有复杂边界的大型图表成为可能，如图1所示。在这个例子中，切割是手工完成的(图1-C)，为方法的健壮性创建一个大型的测试用例。(第3节将展示如何自动将模型切割成圆盘同胚的图表。)

Riemann’s theorem states that for any surface $S$ homeomorphic to a disc, it is possible to find a parameterization of the surface satisfying Equation 1. However, since we want to use the resulting parameterization for texture mapping, we add the constraint that the edges of the triangulation should be mapped to straight lines, and the mapping should vary linearly in each triangle. With this additional constraint, it is not always possible to satisfy the conformality condition. For this reason, we will minimize the violation of Riemann’s condition in the least squares sense.

**黎曼定理**表明，对于任何圆盘同胚的曲面，都有可能找到满足方程1的曲面的参数化。然而，由于我们想要将结果参数化用于纹理映射，我们添加了一个约束条件，即三角形的边缘应该映射到直线，并且映射应该在每个三角形中线性变化。有了这个附加约束，就不可能总是满足适形条件。为此，我们将在最小二乘意义上最小化对黎曼条件的破坏。

## 2.3 Conformality in a Triangulation  三角剖分中的共形

Consider now a triangulation $\mathcal{G}=\{[1,\dots,n],\mathcal{T},(\mathbf{p}_j)_{1\leq j\leq n}\}$ , where $[1,\dots,n],n\ge 3$ , corresponds to the vertices, where $\mathcal{T}$ is a set of $n^{\prime}$ triangles represented by triples of vertices, and where $\mathbf{p}_j\in \Reals^3$ denotes the geometric location at the vertex $j$ . We suppose that each triangle is provided with a local orthonormal basis, where $(x_1,y_1),(x_2,y_2),(x_3,y_3)$ are the coordinates of its vertices in this basis (i.e., the normal is along the $z$-axis). The local bases of two triangles sharing an edge are consistently oriented.

现在考虑一个三角化 $\mathcal{G}=\{[1,\dots,n],\mathcal{T},(\mathbf{p}_j)_{1\leq j\leq n}\}$ ，其中 $[1，\dots,n],n\ge 3$ ，对应于顶点，其中 $\mathcal{T}$ 是 $n^{\prime}$ 个由三个顶点表示的三角形的集合，其中 $\mathbf{p}_j \in \Reals^3$ 表示顶点 $j$ 的几何位置。我们假设每个三角形都有一个局部标准正交基，其中 $(x_1,y_1),(x_2,y_2),(x_3,y_3)$ 是该基中顶点的坐标(即法线沿 $z$ 轴)。共享一条边的两个三角形的局部基底的面朝向是相同的。

We now consider the restriction of $\mathcal{X}$ to a triangle $T$ and apply the conformality criterion to the inverse map $\mathcal{U}:(x,y) \mapsto (u,v)$ (i.e. the coordinates of the points are given and we want their parameterization). In the local frame of the triangle, Equation 1 becomes

我们现在考虑 $\mathcal{X}$ 对三角形 $T$ 的限制，并将共形准则应用到反向映射 $\mathcal{U}:(x,y) \mapsto(u,v)$ (即点的坐标是给定的，我们想要它们的参数化)。在三角形的局部坐标系中，方程1变成
$$
\frac{\partial\mathcal{X}}{\partial u} - i\frac{\partial\mathcal{X}}{\partial v} = 0,
$$

> PS：根据复数定义，$i\frac{\partial\mathcal{X}}{\partial v}$ 相当于把 $\frac{\partial\mathcal{X}}{\partial v}$ 逆时针旋转 90$\degree$，故上式成立。

where $\mathcal{X}$ has been written using complex numbers, i.e. $\mathcal{X}=x+iy$ . By the theorem on the derivatives of inverse functions, this implies that

其中 $\mathcal{X}$ 使用复数写，即 $\mathcal{X}= x +iy$ 。通过反函数的导数定理，这意味着
$$
\frac{\partial\mathcal{U}}{\partial x} + i\frac{\partial\mathcal{U}}{\partial y} = 0, \tag{2}
$$
where $\mathcal{U}= u +iv$ . (This is a concise formulation of the Cauchy-Riemann equations.)

其中 $\mathcal{U}= u +iv$ 。(这是一个简洁的 **Cauchy-Riemann** 方程的公式。)

Since this equation cannot in general be strictly enforced, we minimize the violation of the conformality condition in the least squares sense, which defines the criterion $C$ :

由于该方程一般不能严格执行，我们在最小二乘意义上减少违背共形条件，这就定义了标准 $C$ :
$$
C(T) = \int_T\Bigg| \frac{\partial\mathcal{U}}{\partial x} + i\frac{\partial\mathcal{U}}{\partial y} \Bigg|^2 \, dA = \Bigg| \frac{\partial\mathcal{U}}{\partial x} + i\frac{\partial\mathcal{U}}{\partial y} \Bigg|^2A_T,
$$
where $A_T$ is the area of the triangle and the notation $|z|$ stands for the modulus of the complex number $z$.

其中 $A_T$ 为三角形面积， $|z|$ 表示复数 $z$ 的模。

Summing over the whole triangulation, the criterion to minimize is then

对整个三角剖分求和，求最小的准则为
$$
C(\mathcal{T}) = \sum_{T\in \mathcal{T}} C(T).
$$


## 2.4 Gradient in a Triangle 三角形的梯度

Our goal is now to associate with each vertex $j$ a complex number $U_j$ such that the Cauchy-Riemann equation is satisfied (in the least squares sense) in each triangle. To this aim, let us rewrite the criterion $C(T)$ , assuming the mapping  $\mathcal{U}$ varies linearly in $T$ .

现在，我们的目标是将每个顶点关联到一个复数 $U_j$ ，以便在每个三角形中满足**柯西-黎曼方程**(在最小二乘意义上)。为了达到这个目的，让我们重写标准 $C(T)$ ，假设映射 $\mathcal{U}$ 在 $T$ 中线性变化。

We consider a triangle $\{(x_1,y_1),(x_2,y_2),(x_3,y_3)\}$ of $\Reals^2$ , with scalars $u_1,u_2,u_3$ associated with its vertices. We have:

我们考虑一个三角形 $\{(x_1,y_1)，(x_2,y_2)，(x_3,y_3)\}$  of $\Reals^2$ ，标量 $u_1,u_2,u_3$ 与其顶点相关联。我们有:
$$
\begin{pmatrix}
\partial u/\partial x \\
\partial u/\partial y
\end{pmatrix} = \frac{1}{d_T}
\begin{pmatrix}
y_2-y_3 & y_3-y_1 & y_1-y_2 \\
x_3-x_2 & x_1-x_3 & x_2-x_1
\end{pmatrix} 
\begin{pmatrix}
u_1 \\ u_2 \\ u_3
\end{pmatrix},
$$
where  $d_T=(x_1y_2-y_1x_2)+(x_2y_3-y_2x_3)+(x_3y_1-y_3x_1)$ is twice the area of the triangle. 

其中 $d_T=(x_1y_2-y_1x_2)+(x_2y_3-y_2x_3)+(x_3y_1-y_3x_1)$ 是三角形面积的两倍。

The two components of the gradient can be gathered in a complex number:  

梯度的两个分量可以打包成一个复数:
$$
\frac{\partial u}{\partial x} +i\frac{\partial u}{\partial y}=\frac{i}{d_T}(W_1 \quad W_2\quad W_3)(u_1 \quad u_2 \quad u_3)^T,
$$
where

其中
$$
\begin{cases}
W_1 = (x_3-x_2)+i(y_3-y_2),\\
W_2 = (x_1-x_3)+i(y_1-y_3),\\
W_3 = (x_2-x_1)+i(y_2-y_1).
\end{cases}
$$

> 其实就是写成了复数形式，用实数部和虚数部分别表示 $\partial u/\partial x$ 和 $\partial u/\partial y$ 。

The Cauchy-Riemann equation (Equation 2) can be rewritten as follows:

**柯西-黎曼方程**(式2)可以改写为:
$$
\frac{\partial \mathcal{U}}{\partial x} +i\frac{\partial \mathcal{U}}{\partial y}=\frac{i}{d_T}(W_1 \quad W_2\quad W_3)(U_1 \quad U_2 \quad U_3)^T = 0,
$$
where $U_j = u_j+iv_j$ .

其中 $U_j = u_j+iv_j$ 。

The objective function thus reduces to  

因此，目标函数可以简化为
$$
C(\mathbf{U} = (U_1,\dots,U_n)^T) = \sum_{T\in \mathcal{T}}C(T), \quad \mathrm{with} \\
C(T) = \frac{1}{d_T}\Bigg|(W_{j1,T} \enspace W_{j2,T} \enspace W_{j3,T}) 
(U_{j1} \enspace U_{j2} \enspace U_{j3})^T\Bigg|^2,
$$
where triangle $T$ has vertices indexed by $j_1,j_2,j_3$ . (We have multiplied $C(T)$ by a factor of 2 to simplify the expression.)  

其中三角形 $T$ 的顶点索引为 $j_1,j_2,j_3$ 。(我们将 $C(T)$ 乘以2来简化表达式。)



## 2.5 Least Squares Conformal Maps  

$C(\mathbf{U})$ is quadratic in the complex numbers $U_1,\dots,U_n$ , so can be written down as  

$C(\mathbf{U})$ 是复数 $U_1,\dots,U_n$ 的二次方，因此可以写成
$$
C(\mathbf{U}) = \mathbf{U}^*\mathcal{C} \mathbf{U}, \tag{3}
$$
where $\mathcal{C}$ is a Hermitian symmetric $n\times n$ matrix and the notation $\mathbf{U}^*$ stands for the Hermitian (complex) conjugate of $\mathbf{U}$ . $\mathcal{C}$ is an instance of a Hermitian Gram matrix, i.e. it can be written as

其中 $\mathcal{C}$ 是一个 $n\times n$ 阶 [$Hermite$ 对称矩阵](https://zhuanlan.zhihu.com/p/118207414)，符号 $\mathbf{U}^*$ 表示 $\mathbf{U}$ 的 $Hermite$ (复)共轭。$\mathcal{C}$ 是 $Hermite$ $Gram $ 矩阵的一个实例，即它可以写成
$$
\mathcal{C} = \mathcal{M}^*\mathcal{M},
$$
where $\mathcal{M}=(m_{ij})$ is the sparse $n^{\prime} \times n$ matrix (rows are indexed by triangles, columns are indexed by vertices) whose coefficient is

其中 $\mathcal{M}=(m_{ij})$ 是稀疏的 $n^{\prime} \times n$ 矩阵(行由三角形索引，列由顶点索引)其系数是
$$
m_{ij} = \begin{cases}
\frac{W_{j,T_i}}{\sqrt{d_{T_i}}}  &\text{if vetex}\space j \space\text{belongs to triangle}\space T_i,\\
0 & \text{otherwise.}
\end{cases}
$$
For the optimization problem to have a non-trivial solution, some of the $U_i$‘s must be set to *a priori* values. Let us decompose the vector $\mathbf{U}$ as $(\mathbf{U}_f^T, \mathbf{U}_p^T)^T$ , where $\mathbf{U}_f$ is the vector of *free* coordinates of $\mathbf{U}$ (the variables of the optimization problem) and $\mathbf{U}_p$ is the vector of *pinned* coordinates of $\mathbf{U}$ , of length $p$ ( $p\le n$ ) . Along the same lines, $\mathcal{M}$ can be decomposed in block matrices as

为了使优化问题有一个非平凡的解，一些 $U_i$ 必须被设置为先验值。让我们将向量 $\mathbf{U}$ 分解为 $(\mathbf{U}_f^T， \mathbf{U}_p^T)^T$ ，其中$ \mathbf{U}_f$ 是 $ \mathbf{U}$ (优化问题的变量)的自由坐标的向量，$\mathbf{U}_p$ 是 $\mathbf{U}$ 的固定坐标的向量，长度为 $p$ ( $p\le n$ )。沿着同样的路线，$\mathcal{M}$ 可以在块矩阵中分解为
$$
\mathcal{M} = (\mathcal{M}_f \quad \mathcal{M}_p),
$$
where $\mathcal{M}_f$ is a $n^{\prime} \times (n-p)$ matrix and $\mathcal{M}_p$ is a  $n^{\prime} \times p$ matrix. Now, Equation 3 can be rewritten as

其中 $\mathcal{M}_f$ 是一个 $n^{\prime}\times (n-p)$ 矩阵，$\mathcal{M}_p$ 是一个 $n^{\prime}\times p$ 矩阵。现在，方程3可以改写为
$$
C(\mathbf{U}) = \mathbf{U}^*\mathcal{M}^*\mathcal{M}\mathbf{U} = \|\mathcal{M}\mathbf{U}\|^2 =
\|\mathcal{M}_f\mathbf{U}_f+\mathcal{M}_p\mathbf{U}_p\|^2,
$$
where the notation $\|\mathbf{v}\|^2$ stands for the inner product $<\mathbf{v,\overline{v}}>$ ( $\overline{\mathrm{v}}$  stands for the conjugate of $\mathrm{v}$ ).

其中符号 $\|\mathbf{v}\|^2$ 表示内积 $<\mathbf{v，\overline{v}}>$ ( $\overline{\mathbf{v}}$ 表示 $\mathbf{v}$ 的共轭)。

Rewriting the objective function with only real matrices and vectors yields  

用实矩阵和向量重写目标函数
$$
C(\mathbf{x}) = \|\mathcal{A}\mathbf{x}-\mathbf{b}\|^2, \tag{4}
$$
with

与
$$
\mathcal{A} = \begin{pmatrix}
\mathcal{M}_f^1 & -\mathcal{M}_f^2 \\
\mathcal{M}_f^2 & \mathcal{M}_f^1
\end{pmatrix}, \qquad
\mathbf{b} = -\begin{pmatrix}
\mathcal{M}_p^1 & -\mathcal{M}_p^2 \\
\mathcal{M}_p^2 & \mathcal{M}_p^1
\end{pmatrix}
\begin{pmatrix}
\mathbf{U}_p^1 \\
\mathbf{U}_p^2
\end{pmatrix},
$$


where the superscripts $^1$ and $^2$ stand respectively for the real and imaginary part, $\|\mathbf{v}\|$ stands this time for the traditional $L_2$-norm of a vector with real coordinates and  $\mathbf{v}=(\mathbf{U}_f^{1^T}, \mathbf{U}_f^{2^T})^T$  is the vector of unknowns.

其中上标 $^1$ 和 $^2$ 分别代表实部和虚部， $\|\mathbf{v}\|$ 这次代表一个实坐标向量的传统 $L_2$-范数， $\mathbf{v}=(\mathbf{U}_f^{1^T}， \mathbf{U}_f^{2^T})^T$ 是未知数向量。

Note that $\mathcal{A}$ is a $2n^\prime \times 2(n-p)$ matrix,  $\mathbf{b}$ is a vector of $\reals^{2n^\prime}$ and $\mathbf{x}$ is a vector of $\reals^{2(n-p)}$ (the $u_i$ and $v_i$ coordinates of the vertices in parameter space that are allowed to move freely).

$\mathcal{A}$ 是 $2n^\prime \times 2(n-p)$ 矩阵， $\mathbf{b}$ 是 $\reals^{2n^\prime}$ 的向量， $\mathbf{x}$ 是 $\reals^{2(n-p)}$ 的向量(参数空间中允许自由移动的顶点的 $u_i$ 和 $v_i$ 坐标)。

 

## 2.6 Properties  属性

The above minimization problem has several fundamental properties which are proved in the appendix:

上述最小化问题具有几个基本性质，在附录中得到了证明:

+ The matrix $\mathcal{A}$ has full rank when the number of pinned vertices, i.e. $p$, is larger than or equal to 2.
+ As a consequence, the minimization problem has a unique solution when $p\ge 2$ , given by $\mathbf{x}=(\mathcal{A}^T \mathcal{A})^{-1}\mathcal{A}^T\mathbf{b}$ . The best value for $p$ is 2, since in this case the mapping $\mathcal{U}$ can be fully conformal if the surface is developable (i.e. the minimum of the objective function is zero). In our experiments, we have pinned the two vertices maximizing the length of the shorted path between them (i.e. the graph diameter).
+ The solution to the minimization problem is invariant by a similarity in texture space.
+ The solution to the minimization problem is independent of the resolution of the mesh. This property is illustrated in Figure 3.
+ In texture space, all the triangles are consistently oriented if the pinned vertices are chosen on the boundary of $\mathcal{T}$ . In other words, triangle flips cannot occur.

+ 当固定顶点的个数，即 $p$ 大于等于2时，矩阵 $\mathcal{A}$ 秩满。
+ 因此，当 $p\ge 2$ ，由 $\mathbf{x}=(\mathcal{A}^T \mathcal{A})^{-1}\mathcal{A}^T\mathbf{b}$ 时，最小化问题有唯一解。 $p$ 的最佳值是2，因为在这种情况下，映射 $\mathcal{U}$ 可以是完全共形的，如果曲面是可展的（即，目标函数的最小值为零）。在我们的实验中，我们固定了两个顶点，使它们之间的短路径长度最大化（即图的直径）。
+ 最小化问题的解决方案是不变的相似性在纹理空间。
+ 最小化问题的解决是独立于网格的分辨率。此属性如图3所示。
+ 在纹理空间中，如果固定的顶点选择在 $\mathcal{T}$ 的边界上，所有的三角形都是一致的方向。换句话说，三角翻转不可能发生。



# 3 SEGMENTATION





## 3.1 Detect Features  



## 3.2 Expand Charts  



## 3.3 Validate Charts



# 4 PACKING



# 5 RESULTS  



# CONCLUSION  





# ACKNOWLEDGMENTS  



# A PROPERTIES OF LSCMS

The minimization problem of Section 2 has several interesting properties when the number $p$ of pinned vertices in parameter space is sufficient. In what follows, $\mathcal{T}$ is assumed to be homeomorphic to a disc.

当参数空间中固定顶点的数目为 $p$ 时，第2节的最小化问题有几个有趣的性质。在接下来的内容中， $\mathcal{T}$ 被假定为一个盘的同胚。

## A.1 Full Rank

We first show that the matrices $\mathcal{M}_f$ and $\mathcal{A}$ have full rank when $p\ge2$ ( $p$ denotes the number of pinned vertices).

我们首先证明了当 $p\ge2$ ( $p$ 表示固定顶点的数目)时，矩阵 $\mathcal{M}_f$ 和 $\mathcal{A}$ 具有满秩。

![image-20220727110809724](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202207271108853.png)

For this, recall that a triangulation that is topologically a disc can be incrementally constructed with only two operations (cf. Figure 11): the *glue* operation creates one new vertex and one new face, and the *join* operation creates one new face. Thus, incremental construction creates at most as much vertices as faces. Since the implest triangulation (one triangle) has one face and three vertices, we have that $n^\prime \ge n-2$ (where $n$ denotes the number of vertices, and $n^\prime$ the number of triangles, as in the rest of the paper).

为此，回想一下，一个在拓扑上是一个圆盘的三角测量可以只通过两个操作来增量地构建(参见图11): *glue* 操作创建一个新顶点和一个新面，*join* 操作创建一个新面。因此，增量构造创建的顶点最多与面一样多。因为隐式三角划分(一个三角形)有一个面和三个顶点，我们有 $n^\prime \ge n-2$ (其中 $n$ 表示顶点的数量，而 $n^\prime$ 表示三角形的数量，就像在论文的其他部分一样)。

We first show that the rank of $\mathcal{M}_f$ is $n-p$ when $p \ge 2$ . First ote that since $n^\prime \ge n-2$ , $\min(n^\prime, n-p) = m-p$ if $p \ge 2$ and the rank of $\mathcal{M}_f$ is at most $n-p$ . We assume that $\mathcal{T}$ is incrementally constructed with glue and join operations and prove the result by induction on the size of $\mathcal{M}_f$ . We also assume, without loss of generality, that the $p$ pinned vertices are concentrated in the initial triangulation. Let $n_i^\prime, n_i -p$ be the dimensions of the matrix $\mathcal{M}_f^{(i)}$ at step $i$ . Observe that since $\mathcal{T}$ is a non-degenerate triangulation, none of the coefficients $W_{j,T_i}$ is zero.

我们首先证明了当 $p \ge 2$ 时 $\mathcal{M}_f$ 的秩为 $n-p$ 。首先，由于 $n^\prime \ge n-2$ ，  $\min(n^\prime, n-p) = M -p$ ，如果 $p \ge 2$ ，并且 $\mathcal{M}_f$ 的秩最多为 $n-p$ 。我们假设 $\mathcal{T}$ 是用粘合和连接操作递增构造的，并对 $\mathcal{M}_f$ 的大小进行归纳证明。在不丧失一般性的前提下，我们还假定 $p$ 固定的顶点集中在初始三角剖分中。设 $n_i^\prime, n_i -p$ 是矩阵 $\mathcal{M}_f^{(i)}$ 在步长 $i$ 处的维数。注意，由于 $\mathcal{T}$ 是一个非退化三角化， $W_{j,T_i}$ 的系数都不为零。



 

 



