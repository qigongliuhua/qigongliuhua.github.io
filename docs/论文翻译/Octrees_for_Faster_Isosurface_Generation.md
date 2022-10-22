> Octrees for Faster Isosurface Generation  
>
> 
>
> Jane Wilhelms and Allen Van Gelder  
>
> University of California, Santa Cruz  



# Abstract  

The large size of many volume data sets often prevents visualization algorithms from providing interactive rendering. The use of hierarchical data structures can ameliorate this problem by storing summary information to prevent useless exploration of regions of little or no current interest within the volume. This paper discusses research into the use of the octree hierarchical data structure when the regions of current interest can vary during the application, and are not known a priori. Octrees are well suited to the six-sided cell structure of many volumes.

许多体积数据集形成的大尺寸通常会阻碍可视化算法实现交互式渲染。使用分层数据结构可以通过存储摘要信息来避免对体积中当前很少或没有兴趣的区域进行无用的探索，从而改善此问题。本文讨论了当当前感兴趣的区域在应用过程中可能发生变化，且事先未知时，八叉树分层数据结构的使用。八叉树非常适合许多体积的六面体结构。

A new space-efficient design is introduced for octree representations of volumes whose resolutions are not conveniently a power of two; octrees following this design are called branch-on-need octrees (BONOs). Also, a caching method is described that essentially passes information between octree neighbors whose visitation times may be quite different, then discards it when its useful life is over. 

（我们）提出了一种新的空间效率设计方法，用于体积的八叉树表示，其分辨率不是通常的2的幂次方；遵循这种设计的八叉树称为按需分支八叉树（BONO）。此外，还描述了一种缓存方法，它本质上是在八叉树邻居之间传递信息，而八叉树的访问时间可能会有很大的不同，然后在其使用寿命结束时将其丢弃。

Using the application of octrees to iso-surface generation as a focus, space and time comparisons for octree-based versus more traditional “marching” methods are presented.

以八叉树在等值面生成中的应用为重点，对基于八叉树的方法与更传统的“行进”方法进行了空间和时间比较。



# 1 Introduction  

Interactive visualization is of major importance to scientific users, but the sheer size of volume data sets can tax the resources of computer workstations. Intelligent use of data structures and traversal methods can make a significant difference in algorithm performance. In particular, the use of hierarchical data structures to summarize volume information can prevent useless traversal of regions of little interest. However, the storage and traversal of hierarchical data structures themselves can add to the resource consumption of the algorithm, both in terms of time and space.

交互式可视化对于科学用户来说非常重要，但海量体积数据集的庞大规模会使计算机工作站的资源负担过重。智能地使用数据结构和遍历方法可以显著提高算法性能。特别是，使用分层数据结构来汇总体积信息可以防止对不太感兴趣的区域进行无用的遍历。然而，分层数据结构本身的存储和遍历会增加算法的资源消耗，无论是在时间还是空间方面。

We are exploring the advantages and disadvantages of hierarchical data structures for visualization. In particular, we have explored the use of octrees in conjunction with a cell-oriented iso-surface generation algorithm [27, 13, 26].

我们正在探索用于可视化的分层数据结构的优点和缺点。特别是，我们探索了八叉树与面向单元的等值面生成算法的结合使用[27，13，26]。

Octrees are particularly appropriate for representing sample data volumes common to scientific visualization, where the data points often dene a spatial decomposition into hexahedral, space-filling, nonoverlapping regions. Use of octrees for controlling volume traversal is appropriate whether regions are regular hexahedra (cubes, rectangular parallelopiped), as is common in medical imaging, or the irregular, warped hexahedra (curvilinear decompositions) that are common in computational fluid dynamics. 

八叉树特别适合表示科学可视化常用的样本数据量，其中数据点通常会将空间分解为六面体、空间填充、非重叠区域。无论区域是医学成像中常见的正六面体（立方体、长方体），还是计算流体动力学中常见的不规则、扭曲的六面体，使用八叉树控制体积遍历都是合适的。

A volume whose maximum resolution is between $2^{k-1}$ and $2^k$ can be represented by an octree of depth $k$ . This paper discusses the use of summary information at each node for the entire sub-volume beneath it, making it possible to explore the volume contents without examining every data point. For iso-surface generation the summary information consists of the maximum and minimum values of data within each node's region.

最大分辨率在 $2^{k-1}$ 和 $2^k$ 之间的体积可以用深度为 $k$ 的八叉树表示。本文讨论了在每个节点对其下的整个子体积使用摘要信息，从而可以在不检查每个数据点的情况下探索体积内容。对于等值面的生成，摘要信息由每个节点区域内数据的最大值和最小值组成。



## 1.1 Background and Prior Work  

Octrees, like quadtrees, are hierarchical data structures based on decomposition of space [15, 22, 16, 17, 14, 21, 20]. Quadtrees are two-dimensional decompositions that had their beginnings in the hierarchical representation of digital image data and spatial decomposition for hidden surface elimination [24, 11, 19]. In quadtrees, space is recursively subdivided into four subregions, hence the name “quad”. Octrees are three-dimensional extensions of quadtrees, where space is recursively subdivided into eight sub-volumes, and the root of the octree refers to the entire volume [15, 22, 16, 17]. In the normal case, each coordinate direction is divided in two, giving a “lower” half space and an “upper” half space. The effect of all three divisions is to create octants.

八叉树和四叉树一样，是基于空间分解的分层数据结构[15、22、16、17、14、21、20]。四叉树是二维分解，其起源于数字图像数据的分层表示和隐藏表面消除的空间分解[24，11，19]。在四叉树中，空间递归地细分为四个子区域，因此称为“quad”。八叉树是四叉树的三维扩展，其中空间递归地细分为八个子体积，八叉树的根表示整个卷[15、22、16、17]。在正常情况下，每个坐标方向被分为两个，给出一个“下”半空间和一个“上”半空间。这三个分区的作用都是创建八分位。

Octrees have been used to represent three-dimensional objects [10, 28]. Octrees also have been used just to represent the spatial relationship of geometrical objects, making it relatively simple to accomplish such operations as locating neighbors [18] and to traverse the volume from front to back for hidden surface removal [4, 25].

八叉树被用来表示三维物体[10，28]。八叉树也仅用于表示几何对象的空间关系，使定位邻居[18]和从前向后遍历体积以去除隐藏表面[4，25]等操作相对简单。

In many octree applications, including those mentioned so far, the octree is used to represent some boolean property of the points in the volume, or some property for which most of the points take on a null value that is specified a priori . In image-processing terminology, a point in the volume is “black” (in the object), or “white” (uninteresting). Here we brie y review some storage optimizations that have been developed for such cases, and discuss why they do not carry over to the applications we have, in which the volume data can assume many values (none of which may be “uninteresting” a priori )

在许多八叉树应用程序中，包括到目前为止提到的应用程序，八叉树用于表示卷中点的某些布尔属性，或表示大多数点具有先验指定的空值的某些属性。在图像处理术语中，卷中的点是“黑色”（在对象中）或“白色”（不感兴趣）。在这里，我们简要回顾了针对此类情况开发的一些存储优化，并讨论了为什么它们不会延续到我们现有的应用程序中，在这些应用程序中卷数据可以假定许多值（其中没有一个可能是“不感兴趣”）

When the property is boolean, only one bit per octree node is needed. Levoy described a straightforward implementation for abstracting the (boolean) property of nontransparency from medical image data as part of volume rendering [12]. Initially, his method rounds the volume resolution up to $2^d\times 2^d \times 2^d$ , and assigns 8 data points to each node in the lowest level of the octree. It represents every node at the same level of the octree in a long bit-vector (1 = “black”), where 1 denotes that some child has value 1, or at the lowest level, that some data point is nontransparent among the 8 covered by the octree node. All octree information is located by address calculations; no pointers are needed. The storage overhead is acceptable, well under 20% of the original volume data in practice.

当属性为布尔值时，每个八叉树节点只需要一位。Levoy描述了从医学图像数据中提取不透明度（布尔）属性的简单实现，作为体绘制的一部分[12]。最初，他的方法将体积分辨率四舍五入到 $2^d\times 2^d \times 2^d$ ，并为八叉树最低层次的每个节点分配8个数据点。它把八叉树同一级别的每个节点表示成长的位向量（1=“black”），其中1表示某个子节点的值为1，或者在最低级别，在八叉树节点覆盖的8个节点中，某个数据点是不透明的。所有八叉树信息通过地址计算定位；不需要指针。存储开销是可以接受的，实际上远远低于原始卷数据的20%。

An alternative strategy is to prune lower portions of the octree when their values can be inferred from an ancestor [29]. One method is to dene an internal node as “white” or “black” if all of its descendants are of that color, in which case no storage is allocated to the descendants; this process is called condensation. Otherwise the node is gray and has 8 explicit children. (For static nonboolean properties, only white nodes can be condensed.) How many octree nodes are needed depends on the original data. Because of the irregular shapes possible in such octrees, the structure must be represented explicitly, with pointers being the usual choice. Eight pointers per node use up storage quickly, so this implementation is workable only when the object can be represented with relatively few black and white nodes. However, it is possible to reduce the storage requirement to one pointer per node if all eight children of a node are allocated contiguously.

另一种策略是，当八叉树的较低部分的值可以从祖先推断出来时，将其剪除[29]。一种方法是将内部节点定义为“白色”或“黑色”，如果其所有子节点都是该颜色，则不会为子节点分配存储空间；这个过程称为冷凝。否则，节点为灰色，并且有8个显式子节点。（对于静态非布尔属性，只能压缩白色节点。）需要多少个八叉树节点取决于原始数据。由于这种八叉树中可能存在不规则的形状，因此必须明确表示结构，通常选择指针。每个节点有八个指针，会很快耗尽存储空间，因此只有当对象可以用相对较少的黑白节点表示时，此实现才可行。但是，如果一个节点的所有八个子节点都是连续分配的，则可以将存储需求减少到每个节点一个指针。

Linear octrees were introduced by Gargantini as a way to improve on the storage requirements of condensed, pointer-based octrees [6]. Related linear structures were used by others [16, 23]. Essentially, each “black” node in the condensed octree is assigned a key that encodes the path in the octree from the root to that node (see Section 4.1). Gray and white nodes are not allocated any storage, and the keys of the black nodes are stored in sorted order in one array (hence the name “linear”). Whether a linear octree requires more or less storage space than a bit-vector octree depends on the coherence of the boolean property being represented.

线性八叉树是由Gargantini引入的，作为一种改进压缩的、基于指针的八叉树存储需求的方法[6]。其他人使用了相关的线性结构[16，23]。本质上，压缩八叉树中的每个“黑色”节点都被分配了一个键，该键对八叉树从根到该节点的路径进行编码（参见第4.1节）。灰色和白色节点不分配任何存储空间，黑色节点的密钥按排序顺序存储在一个数组中（因此称为“线性”）。线性八叉树是否比位向量八叉树需要更多或更少的存储空间取决于所表示的布尔属性的一致性。

Glassner describes an implementation related to linear octrees, but with several innovations [8]. He uses a hash table instead of a sorted array to speed up node location by key. His ray tracing application requires storage of gray nodes, so he uses a slightly different key and allocates all 8 children of a node contiguously, so they can all be accessed under one key entry.

Glassner描述了一种与线性八叉树相关的实现，但有一些创新[8]。他使用哈希表而不是排序数组来按键加速节点位置。他的光线跟踪应用程序需要存储灰色节点，因此他使用了一个稍有不同的键，并连续分配节点的所有8个子节点，因此可以在一个键条目下访问所有子节点。

Bloomenthal also uses an octree to organize nonboolean data for implicit surface modeling [3]. A closed-form function is defined over the volume and evaluated by adaptive sampling. A piecewise polygonal representation is derived from the octree. The octree only pertains to the current iso-value, or threshold value, so this application also falls into the category of those whose data has a frequently occurring null value.

Bloomenthal还使用八叉树来组织隐式曲面建模的非布尔数据[3]。在体积上定义闭合形式函数，并通过自适应采样进行评估。从八叉树中导出了分段多边形表示。八叉树只适用于当前iso值或阈值，因此该应用程序也属于那些数据经常出现空值的应用程序。

We are concerned here with the use of octrees to organize nonboolean data, where the points of interest cannot be determined a priori; that is, there is no frequently occurring null value. The reason that the condensation methods just discussed are not applicable in this context soon becomes evident: condensation occurs only when all children of a node have the same value, an event that may never occur in volumetric data such as density fields. We are not dealing with an object, or small set of objects, which occupies a possibly small portion of the volume, but rather a function that is defined throughout the volume. As we shall show in Section 3, without the benefits of large scale condensation, obvious octree designs can easily lead to prohibitive storage overhead.

这里我们关注的是使用八叉树来组织非布尔数据，其中兴趣点不能预先确定；也就是说，没有经常出现的空值。刚才讨论的凝聚方法在这种情况下不适用的原因很快就变得显而易见：只有当节点的所有子节点都具有相同的值时，才会发生凝聚，这种情况在密度场等体积数据中可能永远不会发生。我们处理的不是一个对象或一小组对象，它们可能占据体积的一小部分，而是一个在整个体积中定义的函数。正如我们将在第3节中所示，如果没有大规模凝聚的好处，明显的八叉树设计很容易导致令人望而却步的存储开销。

Globus has independently investigated the use of an octree for isosurface generation [9]. His work is compared with ours in more detail in Sections 3.4 and 6.2. Briey, he solved the storage problems by stopping the octree construction at a higher level, allowing an octree node to cover as many as 32 data points. 

Globus独立研究了使用八叉树生成等值面[9]。第3.4节和第6.2节将他的工作与我们的工作进行了更详细的比较。Briey通过在更高层级停止八叉树构造，允许一个八叉树节点覆盖多达32个数据点，从而解决了存储问题。

