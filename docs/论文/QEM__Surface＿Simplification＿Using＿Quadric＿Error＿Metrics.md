>  **Surface Simplification Using Quadric Error Metrics**
>
> Michael Garland∗ Paul S. Heckbert†  
>
> Carnegie Mellon University  

# 摘要

$\quad$ 计算机图形学中的许多应用程序需要复杂、高度细节模型。然而，实际需要的细节程度可能会有很大差异。为了控制处理时间，通常需要使用近似模型（approximations）来代替过于详细的模型。我们开发了一种曲面简化算法，可以快速生成高质量的多边形模型近似。该算法使用顶点对的迭代收缩来近似模型，并使用二次曲面保持曲面误差近似矩阵。通过收缩任意顶点对（不仅仅是边），我们的算法能够连接模型的未连接区域。这可以促进更好的近似模型，无论是在视觉上还是在几何误差。为了允许拓扑连接，我们的系统还支持非流形曲面模型。

> CR Categories: I.3.5 [Computer Graphics]: Computational Geometry and Object Modeling—surface and object representations  
>
> Keywords: surface simplification, multiresolution modeling, pair contraction, level of detail, non-manifold  



# 1 引言

$\quad$ 许多计算机图形应用程序需要复杂、高度精细的模型来保持令人信服的逼真度。因此，通常以非常高的分辨率创建或获取模型，以适应这种对细节的需要。然而，并不总是需要此类模型的全部复杂性，而且由于使用模型的计算成本与其复杂性直接相关，因此有更简单版本的复杂模型是有用的。当然，我们希望自动生成这些近似模型。最近关于曲面简化算法的工作集中于这一目标。

$\quad$ 与此领域的大多数其他工作一样，我们将重点关注多边形模型的简化。**我们将假设该模型仅由三角形组成**。这意味着不会失去通用性，因为原始模型中的每个多边形都可以在预处理阶段的某一个阶段进行三角化。**为了获得更可靠的结果，当两个面的角点在某一点相交时，应将这些面定义为共享一个顶点，而不是使用两个在空间上碰巧重合的单独顶点**。

$\quad$ 我们开发了一种算法，可以生成此类多边形模型的简化版本。我们的算法基于顶点对的迭代收缩（边收缩的推广）。随着算法的进行，将在当前模型的每个顶点处保持几何误差近似值。这种误差近似用二次矩阵表示。我们算法的主要优点是：

+ 效率：该算法能够快速简化复杂模型。例如，我们的实现可以在15秒内创建70000个面模型的100个面近似值。误差近似也非常紧凑，每个顶点只需要10个浮点数。

+ 质量：我们的算法产生的近似模型保持了原始模型的高保真度。即使经过显著简化，模型的主要特征仍会保留下来。
+ 通用性：与大多数其他曲面简化算法不同，我们的算法能够将模型的未连接区域连接在一起，这一过程我们称为*聚合（aggregation）*。



# 2 背景及相关工作

$\quad$ 多边形曲面简化的目标是将多边形模型作为输入，并生成近似模型（即原始模型的近似模型）作为输出。我们假设输入模型（$M_n$）已经三角化。目标近似模型（$M_g$）将满足某些给定的目标标准，这些标准通常是期望的面数量或最大容忍误差。我们对可用于 *多分辨率建模* 的渲染系统的曲面简化算法感兴趣，即生成具有适合当前上下文的适当细节级别的模型。

$\quad$ 我们不认为必须维护模型的拓扑结构。在某些应用领域，例如医学成像，维护对象拓扑可能至关重要。然而，在渲染等应用领域，拓扑不如整体外观重要。我们的算法既能闭合拓扑洞，又能连接未连接的区域。

$\quad$ 许多以前的简化算法都隐式或显式地假设其输入曲面是流形曲面，并且应该保持流形曲面。让我们强调一下，我们并没有做出这种假设。事实上，聚合过程会定期创建非流形区域。

> 流形是一种曲面，其每个点的无穷小邻域在拓扑上等价于一个圆盘（或有边界流形的半圆盘）

## 2.1 曲面简化

$\quad$ 近年来，曲面简化问题，以及更普遍的多分辨率建模问题，受到了越来越多的关注。已经制定了几种不同的算法来简化曲面。与我们的工作最相关的算法可大致分为3类：

$\quad$ **顶点抽取（Vertex Decimation）。** 施罗德（$\mathrm{Schroeder}$）等人描述一种我们称之为顶点抽取的算法。他们的方法以迭代方式选择要删除的顶点，并删除所有相邻面，并重新形成孔的角度。Soucy and Laurendeau 描述了一种更复杂但本质上相似的算法。虽然它们提供了合理的效率和质量，但这些方法并不真正适合我们的目的。这两种方法都使用顶点分类和重新成角方案，这些方案本质上局限于流形曲面，并且它们小心地维护了模型的拓扑结构。虽然这些是某些领域的重要功能，但它们是多分辨率渲染系统的限制。

$\quad$ **顶点群集（Vertex Clustering）。**罗西格纳克（$\mathrm{Rossignac}$）和 博雷尔（$Borrel$） 描述的算法是少数能够处理任意多边形输入的算法之一。将在原始模型周围放置一个边界框，并将其划分为栅格。在每个单元中，单元的顶点聚集到一个顶点中，模型面也相应更新。此过程可能非常快，并且可能对模型进行剧烈的拓扑更改。然而，虽然网格单元的大小确实提供了几何误差范围，但输出的质量通常很低。此外，由于面数仅由指定的栅格尺寸间接确定，因此很难使用特定的面数构建近似值。生成的精确近似值还取决于原始模型相对于周围栅格的精确位置和方向。这种统一方法很容易推广到使用自适应网格结构，如八叉树。这可以改善简化结果，但它仍然不支持我们所期望的质量和控制。

$\quad$ **迭代边收缩（Iterative Edge Contraction）。**已经发布了几种通过迭代收缩边近似模型的算法（见图1）。这些算法之间的本质区别在于它们如何选择要收缩的边。这类算法的一些著名例子是霍普（$\mathrm{Hoppe}$），罗恩法德（$\mathrm{Ronfard}$）和罗西格纳克（$\mathrm{Rossignac}$），以及古埃齐克（$\mathrm{Gu\acute{e}ziec}$）。这些算法似乎都是为在流形曲面上使用而设计的，尽管可以在非流形曲面上使用边收缩。通过执行连续的边收缩，它们可以闭合物体中的孔，但不能连接未连接的区域。

>  ![image-20220613103633240](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202206131036271.png)
>
> 图1：**边收缩（Edge contraction）。**高亮显示的边收缩为一个点。着色三角形将退化，并在收缩过程中移除。

$\quad$ 如果近似模型位于原始模型的某个距离内并且其拓扑结构保持不变是至关重要的，那么科恩（$\mathrm{Cohen}$）等人的简化包络技术可以与上述简化算法之一结合使用。只要对模型所做的任何修改被限制在包络线内，就可以保持全局误差保证。然而，虽然这提供了很强的误差限制，但该方法本质上局限于可定向流形曲面，并小心地保留了模型拓扑。同样，为了简化渲染，这些通常是限制。

$\quad$ 这些以前开发的算法都没有提供我们所期望的效率、质量和通用性的结合。顶点抽取算法不适合我们的需要；他们很小心地维护模型拓扑，通常采用流形几何体。顶点聚类算法非常通用，速度也非常快。然而，它们对结果的控制较差，这些结果的质量可能相当低。边缘收缩算法不支持聚合。

$\quad$ 我们开发了一种既支持聚合又支持高质量近似的算法。它具有顶点聚类的普遍性以及迭代收缩算法的质量和控制。它还允许比一些更高质量的方法更快的简化。

# 3 通过成对收缩抽取

$\quad$ 我们的简化算法基于顶点对的迭代收缩；以前工作中使用的迭代边收缩技术的推广。一个成对收缩，我们将写出 $(\mathbf{v_1,v_2})\rightarrow \mathbf{\bar{v}}$ ，将顶点 $\mathbf{v_1}$ 和 $\mathbf{v_2}$ 移动到新位置 $\mathbf{\bar{v}}$ ，把相连边连接到 $\mathbf{v_1}$ ，并且删除顶点 $\mathbf{v_2}$ 。随后，将删除退化的任何边或面。收缩的影响很小且高度局限性。如果 $(\mathbf{v_1,v_2})$ 是一个边，那么1或更多面将被删除（见图1）。否则，模型的两个以前独立的部分将在 $\mathbf{\bar{v}}$ 处连接（见图2）。

> ![image-20220613110745454](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202206131107482.png)
>
> 图2：**非边收缩（Non-edge contraction）。**收缩非边的顶点对时，将连接模型的未连接部分。虚线表示两个顶点收缩在一起。

$\quad$ 这种收缩的概念实际上相当普遍；我们可以将一组顶点收缩为一个顶点： $(\mathbf{v_1,v_2,\dots,v_k})\rightarrow \mathbf{\bar{v}}$。这种形式的广义收缩既可以表示成对收缩，也可以表示更一般的操作，如顶点聚类。然而，我们使用成对收缩作为算法的原子操作，因为它是最细粒度的收缩操作。

$\quad$ 从初始模型 $M_n$ 开始，应用一系列成对收缩，直到满足简化目标，并生成最终近似 $M_g$ 。由于每个收缩对应于当前模型的局部增量修改，因此该算法实际上生成了一系列模型 $M_n,M_{n-1},\dots,M_g$ 。因此，一次运行可以生成大量近似模型或多分辨率表示，如渐进网格。

## 3.1 聚合

$\quad$ 我们通过利用一般顶点对收缩获得的主要好处是，该算法能够将以前未连接的模型区域连接在一起。一个潜在的副作用是，它使算法对原始模型的网格连接不太敏感。如果实际上两个面仅在互相重合的顶点处相遇，则该对顶点的收缩将修复初始网格的这一缺点（即合并相近的多余的顶点，从而让两个面真正的连接在一起）。

$\quad$ 在某些应用程序中，例如渲染，拓扑可能不如整体形状重要。考虑图3所示的形状，该形状由规则网格中100个紧密间隔的立方体组成。假设我们想要构建左侧模型的近似值，以便在远处进行渲染。基于边收缩的算法可以闭合对象中的孔，但它们永远不能连接断开连接的组件。在只使用边缘收缩的算法中，各个组件单独简化为零，就像中间的在中间一样。使用成对收缩，可以将各个组件合并到单个对象中，如右侧的模型中所示。结果是一个更加可靠的近似值。

> ![image-20220613112420987](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202206131124022.png)
>
> 图3：左侧是由100个紧密间隔的立方体组成的规则网格。在中间，仅使用边收缩构建的近似显示出不可接受的碎片。在右边，使用更一般的成对收缩来实现聚合的结果更接近原始结果。

## 3.2 对选择

$\quad$ 我们选择在初始化时选择有效对集，并在算法过程中仅考虑这些对。我们的决定基于这样一个假设，即在一个很好的近似值中，点不会远离其原始位置。我们会说一对 $(\mathbf{v_1,v_2})$ 是收缩的有效对，如果：

1. $(\mathbf{v_1,v_2})$ 是一个边，或
2. $\|\mathbf{v_1} - \mathbf{v_2}\| < t$ ，其中 $t$ 是阈值参数。

$\quad$ 使用 $t=0$ 的阈值可以给出一个简单的边缘收缩算法。较高的阈值允许非连接顶点配对。当然，必须谨慎选择这一阈值；如果它太高，可能会连接模型中相距很远的分离的部分，这可能是不需要的，并且可能会产生 $O(n^2)$ 对。

$\quad$ 在迭代收缩过程中，我们必须跟踪有效对集。对于每个顶点，我们将其所属的对集关联起来。当我们进行收缩 $(\mathbf{v_1,v_2})\rightarrow \mathbf{\bar{v}}$ 时，$\mathbf{v_1}$ 不仅获取与 $\mathbf{v_2}$ 相连的所有边，还将 $\mathbf{v_2}$ 中的对集合合并到自己的集合中。有效对中出现的每一个 $\mathbf{v_2}$ 都将替换为 $\mathbf{v_1}$ ，并删除重复对。

# 4 二次曲面逼近误差

$\quad$ 为了在给定迭代期间选择要执行的收缩，我们需要一些收缩成本的概念。为了定义此成本，我们尝试描述每个顶点处的误差。为此，我们将对称的 $4 \times 4$ 矩阵 $\mathbf{Q}$ 与每个顶点相关联，并且我们将顶点 $\mathbf{v} = [v_x \enspace v_y \enspace v_z \enspace 1]^T$ 处的误差定义为二次型 $\Delta(\mathbf{v})=\mathbf{v}^T \mathbf{Q} \mathbf{v}$ 。在第5节中，我们将描述如何构造初始矩阵。注意等价曲面 $\Delta(\mathbf{v}) = \epsilon$ （就是相对于 $\mathbf{Q}$ 的误差为 $\epsilon$ 的所有点的集合）是[二次曲面](https://baike.baidu.com/item/%E4%BA%8C%E6%AC%A1%E6%9B%B2%E9%9D%A2/1943943?fr=aladdin)。 

$\quad$ 对于给定的收缩 $(\mathbf{v_1,v_2})\rightarrow \mathbf{\bar{v}}$ ，我们必须导出一个新的矩阵 $\mathbf{\bar{Q}}$，它近似于 $\mathbf{\bar{v}}$ 处的误差。我们选择使用简单的加法规则 $\mathbf{\bar{Q}}=\mathbf{Q_1+Q_2}$。

$\quad$ 为了进行收缩 $(\mathbf{v_1,v_2})\rightarrow \mathbf{\bar{v}}$ ，我们还必须为 $\mathbf{\bar{v}}$ 选择一个位置。一个简单的方案是选择 $\mathbf{v_1}$ 、$\mathbf{v_2}$ 或 $(\mathbf{v_1+v_2})/2$ ，这取决于其中哪一个产生最小值 $\Delta(\mathbf{\bar{v}})$。然而，最好为 $\mathbf{\bar{v}}$ 找到一个位置能够最小化 $\Delta(\mathbf{\bar{v}})$。由于误差函数 $\Delta$ 是二次函数，求其最小值是一个线性问题。因此，我们通过求解 $\partial \Delta/\partial x = \partial \Delta/\partial y = \partial \Delta/\partial z = 0$ 。这相当于求解：
$$
\begin{array}{c}
\begin{bmatrix}
q_{11} & q_{12} & q_{13} & q_{14} \\
q_{12} & q_{22} & q_{23} & q_{24} \\
q_{13} & q_{23} & q_{33} & q_{34} \\
0 & 0 & 0 & 1
\end{bmatrix}
\mathbf{\bar{v}} = 
\begin{bmatrix}
0 \\ 0 \\ 0 \\ 1
\end{bmatrix}  \\
\\
(\text{可自行求偏导验证:} \mathbf{v}^T \mathbf{Qv} = q_{11}x^2+2q_{12}xy+2q_{13}xz+2q_{14}x+q_{22}y^2\\
2q_{23}yz+2q_{24}y+q_{33}z^2+2q_{34}z+q_{44})
\end{array}
$$
$\quad$ 对于 $\mathbf{\bar{v}}$ 。矩阵的最下面一行为空是因为 $\mathbf{\bar{v}}$ 是一个齐次向量 $—$ $w$ 分量始终为1。假设这个矩阵是可逆的，我们得到
$$
\mathbf{\bar{v}} = 
\begin{bmatrix}
q_{11} & q_{12} & q_{13} & q_{14} \\
q_{12} & q_{22} & q_{23} & q_{24} \\
q_{13} & q_{23} & q_{33} & q_{34} \\
0 & 0 & 0 & 1
\end{bmatrix}^{-1}
\begin{bmatrix}
0 \\ 0 \\ 0 \\ 1
\end{bmatrix} \tag{1}
$$
$\quad$ 如果此矩阵不可逆，我们将尝试沿段 $\mathbf{v_1}\mathbf{v_2}$ 找到最佳顶点。如果这也失败了，我们只能从端点和中点中选择 $\mathbf{\bar{v}}$ 。

## 4.1 算法概要

$\quad$ 我们的简化算法是围绕对收缩和误差二次曲面构建的。当前的实现使用邻接图结构表示模型：顶点、边和面都显式表示并链接在一起。要跟踪有效对集，每个顶点都会维护其所属对的列表。算法本身可以快速总结如下：

1. 计算所有初始顶点的 $\mathbf{Q}$ 矩阵。
2. 选择所有有效对。
3. 计算每个有效对 $(\mathbf{v_1,v_2})$ 的最佳收缩目标 $\mathbf{\bar{v}}$ 。该目标顶点的误差 $\mathbf{\bar{v}}^T (\mathbf{Q_1+Q_2}) \mathbf{\bar{v}}$ 成为收缩该对的成本。
4. 将所有对放在以成本为优先级的堆中，最小成本对位于顶部。
5. 以迭代方式从堆中删除开销最小的对 $(\mathbf{v_1,v_2})$ ，收缩该对，并更新涉及 $\mathbf{v_1}$ 的所有有效对的开销。

剩下的唯一问题是如何计算初始 $\mathbf{Q}$ 矩阵，由此构造误差度量 $\Delta$ 。

# 5 导出误差二次曲面

$\quad$ 为了构造误差二次曲面，我们必须选择一种启发式方法来描述几何误差。我们选择了一种与 $\mathrm{Ronfard}$ 和 $\mathrm{Rossignac}$ *[7]* 给出的启发式方法非常相似的方法。在 *[7]* 之后，我们可以观察到，在原始模型中，每个顶点都是一组平面相交的解，即在该顶点相交的三角形的平面。我们可以将一组平面与每个顶点相关联，我们可以将顶点相对于该集的误差定义为到其平面的距离的平方之和：
$$
\Delta(\mathbf{v}) = \Delta([v_x \enspace v_y \enspace v_z \enspace 1]^{\text{T}}) = \sum\limits_{p \in \text{planes}(\mathbf{v})}(\mathbf{p^T v})^2 \tag{2}
$$
$\quad$ 式中， $\mathbf{p} = [a \enspace b \enspace c \enspace d]^T$ 表示由方程式 $ax+by+cz+d=0$ 定义的平面，其中 $a^2+b^2+c^2=1$。这个近似误差度量与 *[7]* 相似，尽管我们在平面集上使用了求和而不是最大值。顶点处的平面集初始化为在该顶点处相交的三角形的平面。请注意，如果我们像 *[7]* 那样显式跟踪这些平面集，我们将在收缩  $(\mathbf{v_1,v_2})\rightarrow \mathbf{\bar{v}}$ 后使用规则：$\text{planes}(\mathbf{\bar{v}}) = \text{planes}(\mathbf{v_1})\cup \text{planes}(\mathbf{v_2}) $ 传播平面。这可能需要相当大的存储量，而且存储量不会随着简化的进行而减少。

$\quad$**（2）**中给出的误差度量可以重写为二次型：
$$
\begin{aligned}
\Delta(\mathbf{v})\quad & = \quad \sum\limits_{\mathbf{p}\in \text{planes}(\mathbf{v})} \mathbf{(v^T p)(p^T v)} \\
& = \quad \sum\limits_{\mathbf{p}\in \text{planes}(\mathbf{v})} \mathbf{v^T (pp^T) v} \\
& = \quad \mathbf{v^T}\Big(\sum\limits_{\mathbf{p}\in \text{planes}} \mathbf{K_p}   \Big) \mathbf{v}

\end{aligned}
$$
$\quad$ 其中 $\mathbf{K_p}$ 是矩阵：
$$
\mathbf{K_p = pp^T} =\begin{bmatrix}
a^2 & ab & ac & ad \\
ab & b^2 & bc & bd \\
ac & bc & c^2 & cd \\
ad & bd & cd & d^2
\end{bmatrix}
$$
$\quad$ 这个*基本误差二次曲面* $\mathbf{K_p}$ 可以用来求空间中任意点到平面 $\mathbf{p}$ 的平方距离。我们可以将这些基本二次曲面求和，并用一个矩阵 $\mathbf{Q}$ 表示整个平面集。

$\quad$ 我们使用单个矩阵隐式跟踪平面集；我们只需添加两个二次曲面（$\mathbf{Q_1+Q_2}$）而不是计算集合并集（$\text{planes}(\mathbf{v_1})\cup \text{planes}(\mathbf{v_2})$）。如果原始度量中由 $\mathbf{Q_1}$ 和 $\mathbf{Q_2}$ 表示的集合不相交，则二次加法等价于集合并集。如果存在一些重叠，则可以多次计算单个平面。但是，任何单个平面最多可以计数3次，因为每个平面最初仅分布到其定义三角形的顶点。这可能会给误差测量带来一些不精确性，但它有主要的好处：空间跟踪平面集所需的时间仅为4×4对称矩阵（10个浮点数）所需的时间，更新近似值的成本仅为添加两个这样的矩阵所需的时间。如果我们愿意牺牲一些额外的存储，甚至可以使用*包含排除公式*消除这种多次计数。

$\quad$ 因此，为了计算我们的成对收缩算法所需的初始 $\mathbf{Q}$ 矩阵，每个顶点必须累积在该顶点处相交的三角形的平面。对于每个顶点，这组平面定义了几个基本误差二次曲面 $\mathbf{K_p}$ 。该顶点的误差二次曲面 $\mathbf{Q}$ 是基本二次曲面的和。请注意，每个顶点的初始误差估计为0，因为每个顶点都位于其所有关联三角形的平面中。

## 5.1 几何解释

$\quad$ 正如我们将看到的，基于平面的误差二次曲面生成了相当高质量的近似值。此外，它们还具有有用的几何意义。

$\quad$ 这些二次曲面的水平面几乎总是椭球体。在某些情况下，水平面可能退化。例如，平行平面（例如，围绕平面曲面区域）将生成两个平行平面的水平曲面，而所有平行于直线的平面（例如，围绕线性曲面折痕）将生成圆柱形水平曲面。只要水平面是非退化椭球体，用于寻找最佳顶点位置的矩阵（*等式1*）将是可逆的。在这种情况下， $\mathbf{\bar{v}}$ 将位于椭球体的中心。

​	

# 6 额外细节

$\quad$ 迄今为止概述的通用算法在大多数模型上表现良好。但是，有一些重要的增强功能可以提高其在某些类型模型上的性能，尤其是具有开放边界的平面模型。

$\quad$ **保留边界（Preserving Boundaries  ）。**前面导出的误差二次曲面不考虑开放边界。对于地形高度场等模型，有必要保留边界曲线，同时简化其形状。我们也可能希望保留离散的颜色不连续性。在这种情况下，我们最初将每条边标记为法线或“不连续”。对于围绕特定不连续边的每个面，我们生成一个穿过该边的垂直平面。然后将这些约束平面转换为二次曲面，通过较大的惩罚因子进行加权，并将其添加到边端点的初始二次曲面中。我们发现这很有效。

$\quad$ **防止网格反转（Preventing Mesh Inversion）**。成对收缩不一定保持收缩区域中面的方向。例如，可以收缩边并使一些相邻面相互折叠。通常，最好避免这种类型的网格反转。我们使用的方案基本上与其他人之前的方案相同（例如 *[7]* ）。在考虑可能的收缩时，我们比较收缩前后每个相邻面的法线。如果正常的翻转，这种收缩可能会受到严重的惩罚或被禁止。

## 6.1 评估近似值

$\quad$ 为了评估我们的算法产生的近似值的质量，我们需要一个比算法本身使用的启发式误差度量更严格的误差度量。我们选择了一个度量标准，用于测量近似值和原始模型之间的平均平方距离。这与 $\mathrm{Hoppe}$ 等人 *[4]* 使用的 $E_{dist}$ 能量项非常相似。我们将简化模型 $M_i$ 的近似误差 $E_i=E(M_n,M_i)$ 定义为：
$$
E_i=\frac{1}{|X_n|+|X_i|}\Bigg(
\sum\limits_{v\in X_n} d^2(v, M_i) + \sum\limits_{v\in X_i} d^2(v, M_n)
\Bigg)
$$
$\quad$ 其中，$X_n$ 和 $X_i$ 是分别在模型 $M_n$ 和 $M_i$ 上采样的点集。距离 $d(v,M)=min_{p\in M}\|V-P\|$ 是从 $V$ 到 $M$ 最近面的最小距离（$\|\sdot\|$是常用的欧几里德向量长度操作符）。我们仅将此指标用于评估目的；它在实际算法中不起作用。

# 7 结果

偷个懒，不翻译了。。。



# 8 讨论

$\quad$ 我们的算法提供了早期算法所没有的效率、质量和通用性。虽然某些其他算法比我们的算法更快或生成更高质量的近似值，但它们通常不符合我们算法在所有三个方面的能力。唯一能够简化任意多边形模型的算法是顶点聚类 *[8]* ，它不能可靠地生成高质量的近似值。可用的高质量方法 *[2、7、3]* 都不支持聚合。 *[2]* 和 *[3]* 似乎都比我们的算法更耗时。 *[7]* 的结果与我们的结果最为相似，因为我们使用了非常相似的误差近似。然而，我们的系统使用了一种更有效的方法来跟踪平面集，并且它包含了一些增强功能，例如边界保持。

$\quad$ 我们的算法还有许多方面有待改进。我们使用了一个非常简单的方案来选择有效对。更复杂的自适应方案很可能会产生更好的结果。我们尚未解决颜色等表面特性的问题。一种可能的解决方案是将每个顶点视为向量 $(x,y,z,r,g,b)$ ，构造 $7\times7$ 二次曲面，并进行简化。我们相信这可以很好地工作，但增加的大小和复杂性使得它不如基本算法那么吸引人。

$\quad$ 虽然我们的算法通常表现良好，但它有几个明显的弱点。首先，如前所述，测量误差作为到一组平面的距离仅在适当的局部邻域中有效。第二，二次曲面中积累的信息本质上是隐式的，有时可能会有问题。假设我们将两个立方体连接在一起，并希望删除与现已失效的内部面相关的平面。通常，不仅很难确定哪些面是不存在的，而且没有明确的方法可以可靠地从二次曲面中删除适当的平面。因此，我们的算法在简化和聚合方面没有我们所希望的那么好。

# 9 结论

$\quad$ 我们描述了一种能够快速生成多边形模型高保真近似值的曲面简化算法。我们的算法使用迭代对收缩来简化模型，并使用二次误差度量来跟踪模型简化时的近似误差。与最终顶点一起存储的二次曲面也可用于描述曲面的整体形状。

$\quad$ 我们的算法能够连接模型的未连接部分，同时仍然保持相当高的质量。虽然大多数以前的算法本身也局限于流形曲面，但我们的系统能够处理和简化非流形对象。最后，我们的算法提供了一个有用的中间地带，介于非常快速、低质量的方法（如顶点聚类 *[8]* ）和非常缓慢、高质量的方法（如网格优化 *[3]* ）之间。



# 引用

[1]  Jonathan Cohen, Amitabh Varshney, Dinesh Manocha, Greg Turk, Hans Weber, Pankaj Agarwal, Frederick Brooks, and William Wright. Simplification envelopes. In *SIGGRAPH ’96 Proc.*, pages 119–128, Aug. 1996.  http://www.cs.unc.edu/∼geom/envelope.html.



[2]  Andr$\mathrm{\acute{e}}$ Gu$\mathrm{\acute{e}}$ziec. Surface simplification with variable tolerance. In *Second Annual Intl. Symp. on Medical Robotics and Computer Assisted Surgery (MRCAS ’95)*, pages 132–139, November 1995.  



[3]  Hugues Hoppe. Progressive meshes. In *SIGGRAPH ’96 Proc.*, pages 99–108, Aug. 1996.  http://www.research.microsoft.com/research/graphics/hoppe/.  



[4]  Hugues Hoppe, Tony DeRose, Tom Duchamp, John McDonald, and Werner Stuetzle. Mesh optimization. In *SIGGRAPH ’93 Proc.*, pages 19–26, Aug. 1993.  http://www.research.microsoft.com/research/graphics/hoppe/.  



[5]  Alan D. Kalvin and Russell H. Taylor. Superfaces:polygonal mesh simplification with bounded error. *IEEE Computer Graphics and Appl.*, 16(3), May 1996.   http://www.computer.org/pubs/cg&a/articles/g30064.pdf.



[6]  David Luebke and Carl Erikson. View-dependent simplification of arbitrary polygonal environments. In *SIGGRAPH 97 Proc.*, August 1997.  



[7]  R$\mathrm{\acute{e}}$mi Ronfard and Jarek Rossignac. Full-range approximation of triangulated polyhedra. *Computer Graphics Forum*, 15(3), Aug. 1996. Proc. Eurographics ’96.  



[8]  Jarek Rossignac and Paul Borrel. Multi-resolution 3D approximations for rendering complex scenes. In B. Falcidieno and T. Kunii, editors, *Modeling in Computer Graphics: Methods and Applications*, pages 455–465, 1993.  



[9]  William J. Schroeder, Jonathan A. Zarge, and William E. Lorensen. Decimation of triangle meshes. *Computer Graphics (SIGGRAPH ’92 Proc.)*, 26(2):65–70, July 1992.  



[10]  Marc Soucy and Denis Laurendeau. Multiresolution surface modeling based on hierarchical triangulation. *Computer Vision and Image Understanding*, 63(1):1–14, 1996.
