# 1 前言

$\quad$ QEM：Quadric Error Metrics。二次度量误差。是一种局部迭代曲面简化算法，优点是简化过后的网格尽可能保留原始模型的特征，可以将模型未连接的区域聚合到一起，速度较快。

## 1.1 聚合

$\quad$ 一个成对收缩，我们将写出 $(\mathbf{v_1,v_2})\rightarrow \mathbf{\bar{v}}$ ，将顶点 $\mathbf{v_1}$ 和 $\mathbf{v_2}$ 移动到新位置 $\mathbf{\bar{v}}$ ，把相连边连接到 $\mathbf{v_1}$ ，并且删除顶点 $\mathbf{v_2}$ 。随后，将删除退化的任何边或面。收缩的影响很小且高度局限性。如果 $(\mathbf{v_1,v_2})$ 是一个边，那么1或更多面将被删除（见图1）。否则，模型的两个以前独立的部分将在 $\mathbf{\bar{v}}$ 处连接（见图2）。

![image-20220613110745454](https://qglh-tuchuang.oss-cn-hangzhou.aliyuncs.com/markdown_img/202206131742727.png)

## 1.2 对选择

$\quad$ 我们选择在初始化时选择有效对集，并在算法过程中仅考虑这些对。我们的决定基于这样一个假设，即在一个很好的近似值中，点不会远离其原始位置。我们会说一对 $(\mathbf{v_1,v_2})$ 是收缩的有效对，如果：

1. $(\mathbf{v_1,v_2})$ 是一个边，或
2. $\|\mathbf{v_1} - \mathbf{v_2}\| < t$ ，其中 $t$ 是阈值参数。

$\quad$ 使用 $t=0$ 的阈值可以给出一个简单的边缘收缩算法。较高的阈值允许非连接顶点配对。当然，必须谨慎选择这一阈值；如果它太高，可能会连接模型中相距很远的分离的部分，这可能是不需要的，并且可能会产生 $O(n^2)$ 对。

$\quad$ 在迭代收缩过程中，我们必须跟踪有效对集。对于每个顶点，我们将其所属的对集关联起来。当我们进行收缩 $(\mathbf{v_1,v_2})\rightarrow \mathbf{\bar{v}}$ 时，$\mathbf{v_1}$ 不仅获取与 $\mathbf{v_2}$ 相连的所有边，还将 $\mathbf{v_2}$ 中的对集合合并到自己的集合中。有效对中出现的每一个 $\mathbf{v_2}$ 都将替换为 $\mathbf{v_1}$ ，并删除重复对。



# 2 算法细节

## 2.1 初始化

### 2.1.1 初始化每个顶点的Q矩阵

$\quad$ 对于每个顶点 $\mathbf{v_i}$，与其相连的三角面集合为 $\text{planes}(\mathbf{v_i})$ ，则每个顶点的 $\mathbf{Q} = \displaystyle\sum\limits_{\mathbf{p}\in \text{planes}(\mathbf{v_i})}\mathbf{K_p}$ 。其中 ：
$$
\mathbf{K_p = pp^T} =\begin{bmatrix}
a^2 & ab & ac & ad \\
ab & b^2 & bc & bd \\
ac & bc & c^2 & cd \\
ad & bd & cd & d^2
\end{bmatrix}
$$
$\quad$ 式中 $\mathbf{p}=[a \enspace b \enspace c \enspace d]^T$ 表示与顶点 $\mathbf{v_i}$ 与相连的某个三角面所处的平面的一般式（$ax+by+cz+d=0$）的系数。且满足 $a^2+b^2+c^2=1$ 。

## 2.1.2 初始化顶点对

$\quad$ $(\mathbf{v_1,v_2})$ 选取规则如下：

1. $(\mathbf{v_1,v_2})$ 是一个边，或
2. $\|\mathbf{v_1} - \mathbf{v_2}\| < t$ ，其中 $t$ 是阈值参数。



## 2.1.3 计算收缩成本以及目标点位置

$\quad$ 为每个有效对确定最佳收缩目标 $\mathbf{\bar{v}}$ 。并确定目标顶点的收缩成本  $\Delta(\mathbf{\bar{v}}) =\mathbf{\bar{v}}^T (\mathbf{Q_1+Q_2}) \mathbf{\bar{v}}$ 。确定收缩目标 $\mathbf{\bar{v}}$ 的方法有：

1. 收缩成本 $\Delta(\mathbf{\bar{v}})$ 是二次曲面，故对 $x,y,z$ 求偏导，令偏导等于零即可得到 $\mathbf{\bar{v}}$ ：
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
   \end{bmatrix} \tag{1},\qquad [q_{ij}] = \mathbf{Q_1+Q_2=\bar{Q}}
   $$
   

2. 如果（1）中矩阵不可逆，则选取 $\mathbf{v_1}$ 、 $\mathbf{v_2}$ 或  $(\mathbf{v_1+v_2})/2$  中成本最小的一个。

## 2.1.4 迭代更新网格

$\quad$ 将所有对放在以成本为优先级的小根堆中，每次迭代从堆中删除开销最小的对 $(\mathbf{v_1,v_2})$ ，然后收缩该对，并更新涉及  $\mathbf{v_1}$ 的所有有效对的开销。



# 3 程序设计

```cpp
Matrix computeQ(Vertex& v);
double computeCost(Vertex& v, Matrix Q);
vec4 findVAndComputeCost(VertexPair &my_pair);

void QEMSurfaceSimplify(Mesh &mesh){
    struct VertexPair{
        Vertex v1, v2;   
        vec4 v;
        Matrix Q1, Q2;
        bool isDelete;
        double cost;
    };
    struct cmp {
        // 升序排列
		bool operator()(const VertexPair& v1, const VertexPair& v2) {
			return v1.cost > v2.cost;
		}
	};
    typedef priority_queue<VertexPair*, vector<VertexPair*>, cmp> pQueue;
    
    pQueue p;
    vector<Vertex>& all_vertexes = mesh.vertexes();
    const double lambda = 0;
    int iter_num = all_vertexes.size() / 2; //删除一半顶点

    map<Vertex, vector<VertexPair*>> connectedPairs;
    map<Vertex, Matrix> mapQ;
    // 初始化所有Q
    for(auto &v : all_vertexes){
        mapQ[v] = computeQ(v);
    }
    // 选择有效对
    for(int i=0; i<all_vertexes.size()-1;++i){
        for(int j=i+1; j<all_vertexes.size();++j){
            auto v1 = all_vertexes[i];
            auto v2 = all_vertexes[j];
			// 如果是相连顶点或者距离相近
            if(	mesh.isConnected(v1, v2)|| v1.distance(v2) < lambda){
                // 初始化新对
                VertexPair new_pair;
                new_pair.v1 = v1;
                new_pair.v2 = v2;
                new_pair.isDelete = false;
                new_pair.Q1 = mapQ[v1];
                new_pair.Q2 = mapQ[v2];
                findVAndComputeCost(new_pair);	// 计算v和相应的代价
                connectedPairs[v1].push_back(&new_pair); //建立v1到所处顶点对的映射
                connectedPairs[v2].push_back(&new_pair); //建立v2到所处顶点对的映射
                p.push(&new_pair);
            }
        }
    }
    // 迭代删除代价最小的对
    while(p.size() && iter_num){
        auto this_pair = p.top();
        p.pop();
        // 如果顶点对已被删除则继续
        if(this_pair->isDelete)
            continue;
        iter_num--;
        // 合并顶点到某个位置
        Vertex &newVertex = mergeVertexesToPos(this_pair->v, this_pair->v1, this_pair->v2);
        
        // 重新生成新的顶点对
        for(auto old_pair : connectedPairs[this_pair->v1]){
            if(old_pair->isDelete)
                continue;
            old_pair->isDelete = true;
            auto otherVertex = old_pair->v1==this_pair->v1?old_pair->v2:old_pair->v1;
            auto otherQ = old_pair->v1==this_pair->v1?old_pair->Q2:old_pair->Q1;
            auto newQ = (old_pair->Q1+old_pair->Q2)/2;
            // 初始化新对
            VertexPair new_pair;
			new_pair.v1 = newVertex;
            new_pair.v2 = otherVertex;
            new_pair.isDelete = false;
            new_pair.Q1 = newQ;
            new_pair.Q2 = otherQ;
            findVAndComputeCost(new_pair);	// 计算v和相应的代价
            connectedPairs[v1].push_back(&new_pair); //建立v1到所处顶点对的映射
            connectedPairs[v2].push_back(&new_pair); //建立v2到所处顶点对的映射
            p.push(&new_pair);
        }
        
        for(auto old_pair : connectedPairs[this_pair->v2]){
            if(old_pair->isDelete)
                continue;
            old_pair->isDelete = true;
            auto otherVertex = old_pair->v2==this_pair->v2?old_pair->v1:old_pair->v2;
            auto otherQ = old_pair->v2==this_pair->v2?old_pair->Q1:old_pair->Q2;
            auto newQ = (old_pair->Q1+old_pair->Q2)/2;
            // 初始化新对
            VertexPair new_pair;
			new_pair.v1 = newVertex;
            new_pair.v2 = otherVertex;
            new_pair.isDelete = false;
            new_pair.Q1 = newQ;
            new_pair.Q2 = otherQ;
            findVAndComputeCost(new_pair);	// 计算v和相应的代价
            connectedPairs[v1].push_back(&new_pair); //建立v1到所处顶点对的映射
            connectedPairs[v2].push_back(&new_pair); //建立v2到所处顶点对的映射
            p.push(&new_pair);
        }
    }
}

```

