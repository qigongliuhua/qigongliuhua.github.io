# 简述

Voronoi图是通过Delaunay三角网获得的，因此需要首先获得Delaunay三角网。



# 1 从平面点集获取Delaunay三角网

这里使用Bowyer逐点插入法获得三角网，该算法简单易懂。

以四个点A、B、C、D举例，首先建立一个超级三角形PQR，这个三角形要把所有点都包含进去。

![img](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091113787.png)

 接着分析A点，因为A点在三角形PQR的外接圆内部，所以利用A点将三角形PQR分拆成三个子三角形。

![img](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091113942.png)

再考虑Ｂ点，它只在三角形AQR的内部，再将三角形AQR分拆成三个子三角形。

![img](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091114173.png)



接着是C点，这时我们有5个三角形，对这5个三角形每一个检查C点在不在它的外接圆内。经过检测，发现它在三角形APR和三角形ABR的外接圆内。

![img](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091114613.png)



 删除三角形APR和三角形ABR的公共边AR，得到四边形ABPR，并将C点与每一个边组成一个三角形。

![img](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091114804.png)



最后对D点进行分析，它在三角形ABC和三角形BCR的外接圆内，所以应删除公共边BC，再用D点与这两个三角形的其他边形成子三角形。

![img](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091114788.png)



![img](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091114522.png)



最后把含有超级三角形的顶点的三角形全部删除，就得到这四个点的三角剖分

![img](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091115351.png)



实际使用时不建议删除超级三角形，因为加上超级三角形可以方便其他算法得到统一。

在删除公共边的时候可以把所有外接圆包含该点的三角形的边汇总起来，最后统一删除，剩下的边再和该点一起组成新面即可。





# 2 由Delaunay三角网得到Voronoi图

首先需要确定Voronoi图的边界，需要如果外心在边界外则需要截取。

这里的Delaunay三角网是保留超级三角形的，这样可以把算法统一为仅对网格内部点操作。

逐点计算1领域内的共面点的中垂线的交点，如果交点在边界外部则需要截取。将所有交点按照顺时针或者逆时针的顺序组织起来作为一个Voronoi单元格。



![image-20220809112453572](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091124615.png)





![image-20220809112520057](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091125086.png)





# 3 Lloyd算法



![image-20220809112453572](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091126516.png)



上图中的红点为采样点，黑点为对应Voronoi单元格的重心，算法的流程就是把红点移到黑点处，然后重新进行Voronoi三角剖分，如此迭代多次直到比较稳定。



![image-20220809112812451](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202208091128488.png)

