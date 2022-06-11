## 1. 排版基础

### 1.1 行内和行间公式

---

你好公式：$a^2 + b^2 = c^2$

---

```latex
a^2 + b^2 = c^2 \tag{equation}
```

$$
a^2 + b^2 = c^2 \tag{equation}
$$

---

$$
a^2 + b^2 = c^2
$$

---

### 1.2 数学模式

​	特点：

+ 输入的空格被忽略。数学符号的间距默认由符号的性质决定。需要人为引入时，使用`\quad`和`\qquad`等命令。
+ 不允许有空行（分段）。
+ 所有的字母被当作数学公式中的变量处理。如果现在数学公式中输入正体的文本，简单情况下可用`\mathrm`。或者用amsmath提供的`\text`命令。



## 2. 数学符号

### 2.1 一般符号

```latex
a_1,a_2,\dots,a_n\\
a_1+a_2+a_3+\dots+a_n
```

$$
a_1,a_2,\dots,a_n\\
a_1+a_2+a_3+\dots+a_n
$$

### 2.2 指数、上下标和导数

​	`^`和`_`指明上下标，一般需要将上下标的把内容用`{}`括起来，否则只能对后面一个符号起作用

```latex
p^3_{ij} \qquad
m_\text{Kunth} \qquad
m_{Kunth} \qquad
\sum_{k=1}^3 k \\[5pt]
a^x+y \neq a^{x+y} \qquad
e^{x^2} \neq {e^x}^2
```

$$
p^3_{ij} \qquad
m_\text{Kunth} \qquad
m_{Kunth} \qquad
\sum_{k=1}^3 k \\[5pt]
a^x+y \neq a^{x+y} \qquad
e^{x^2} \neq {e^x}^2
$$
`	\text`命令仅适合在公式中穿插少量的文字



### 2.3 分式和根式

​	分式使用 `\frac{分子}{分母} `来书写。分式的大小在行间公式中是正常大小，而在行内被极度压缩。 amsmath 提供了方便的命令 `\dfrac `和 `\tfrac`，令用户能够在行内使用正常大小的分式，或是反过来  。

```latex
3/8 \qquad
\frac{3}{8} \qquad
\tfrac{3}{8}\qquad
\dfrac{3}{8}
```

$$
3/8 \qquad
\frac{3}{8} \qquad
\tfrac{3}{8}\qquad
\dfrac{3}{8}
$$
​	一般的根式使用`\sqrt{...}`；表示 n 次方根时写成 `\sqrt[n]{...}`。  

```latex
\sqrt{x} \Leftrightarrow x^{1/2} \qquad
\sqrt[3]{2} \qquad
\sqrt{x^{2} + \sqrt{y}}
```

$$
\sqrt{x} \Leftrightarrow x^{1/2} \qquad
\sqrt[3]{2} \qquad
\sqrt{x^{2} + \sqrt{y}}
$$
​	特殊的分式形式，如二项式结构，由 amsmath 宏包的 `\binom` 命令生成：  

```latex
\binom{n}{k}
```

$$
\binom{n}{k}
$$


### 2.4 关系符

​	LATEX 常见的关系符号除了可以直接输入的 `=`，` >`，`<`，其它符号用命令输入，常用的有不等号 $\ne$(`\ne`)、大于等于号 $\ge$(`\ge`) 和小于等于号 $\le$(`\le`)、约等号 $\approx$ (`\approx`)、等价 $\equiv$(`\equiv`)、正比 $\propto$ (`\propto`)、相似 $\sim$ (`\sim`) 等等。更多符号命令可参考表。
​	**LATEX 还提供了自定义二元关系符的命令 `\stackrel`，用于将一个符号叠加在原有的二元关系符之上:**

```latex
\stackrel{*}{\approx} \qquad \stackrel{=}{\le}
```

$$
\stackrel{*}{\approx} \qquad \stackrel{=}{\le}
$$

### 2.5 算符

​	LATEX 中的算符大多数是二元算符，除了直接用键盘可以输入的 `+`、 `-`、 `∗`、 `=`，其它符号用命令输入，常用的有乘号 $\times$(`\times`)、除号 $\div$(`\div`)、点乘 $\cdot$(`\cdot`)、加减号 $\pm$ (`\pm`) / $\mp$(`\mp`) 等等。更多符号命令可参考表。
​	$\nabla$(`\nabla`) 和 $\partial$ (`\partial`) 也是常用的算符，虽然它们不属于二元算符。LATEX 将数学函数的名称作为一个算符排版，字体为直立字体。其中有一部分符号在上下位置可以书写一些内容作为条件，类似于后文所叙述的巨算符。  



<center><b>Latex作为算符的函数名字一览(不带上下限的算符)</b></center>

|  函数   | 公式  |   函数    |  公式   |   函数    |  公式   |   函数    |  公式   |
| :-----: | :---: | :-------: | :-----: | :-------: | :-----: | :-------: | :-----: |
| $\sin$  | \sin  | $\arcsin$ | \arcsin |  $\sinh$  |  sinh   |  $\exp$   |  \exp   |
| $\dim$  | \dim  |  $\cos$   |  \cos   | $\arccos$ | \arccos |  $\cosh$  |  \cosh  |
| $\log$  |  log  |  $\ker$   |  \ker   |  $\tan$   |  \tan   | $\arctan$ | \arctan |
| $\tanh$ | \tanh |   $\lg$   |   \lg   |  $\hom$   |  \hom   |  $\cot$   |   cot   |
| $\arg$  | \arg  |  $\coth$  |  \coth  |   $\ln$   |   \ln   |  $\deg$   |  \deg   |
| $\sec$  | \sec  |  $\csc$   |  \csc   |           |         |           |         |

<center><b>Latex作为算符的函数名字一览(带上下限的算符)</b></center>

|  函数  | 公式 |   函数    |  公式   |   函数    |  公式   |  函数  | 公式 |
| :----: | :--: | :-------: | :-----: | :-------: | :-----: | :----: | :--: |
| $\lim$ | \lim | $\limsup$ | \limsup | $\liminf$ | \liminf | $\sup$ | \sup |
| $\inf$ | \inf |  $\min$   |  \min   |  $\max$   |  \max   | $\det$ | \det |
| $\Pr$  | \Pr  |  $\gcd$   |  \gcd   |           |         |        |      |

```latex
\lim_{x \rightarrow 0}
\frac{\sin x}{x}=1
```


$$
\lim_{x \rightarrow 0}
\frac{\sin x}{x}=1
$$
​	对于求模表达式， LATEX 提供了 `\bmod` 和 `\pmod` 命令，前者相当于一个二元运算符，后者作为同余表达式的后缀：

```latex
a \bmod b\\
x \equiv a \pmod{b}
```

$$
a \bmod b\\
x \equiv a \pmod{b}
$$
​	如果算符不够用的话， amsmath 允许用户用` \DeclareMathOperator` 定义自己的算符，其中带星号的命令定义带上下限的算符：  

```latex
// 网页端无法正常使用，typora可以正常使用
\DeclareMathOperator{\argh}{argh}
\DeclareMathOperator*{\nut}{Nut}
\argh 3 = \nut_{x=1} 4x
```

$$
\DeclareMathOperator{\argh}{argh}
\DeclareMathOperator*{\nut}{Nut}
\argh 3 = \nut_{x=1} 4x
$$

### 2.6 巨算符

​	积分号 $\int$(`\int`)、求和号 $\sum$ (`\sum`) 等符号称为巨算符。巨算符在行内公式和行间公式的大小和形状有区别。  

行内：$\sum_{i=1}^n \quad \int_0^{\frac{\pi}{2}} \quad \prod_\epsilon$

行间：

```latex
\sum_{i=1}^n \quad \int_0^{\frac{\pi}{2}} \quad \prod_\epsilon
```

$$
\sum_{i=1}^n \quad \int_0^{\frac{\pi}{2}} \quad \prod_\epsilon
$$
​	巨算符的上下标位置可由` \limits` 和` \nolimits` 调整，前者令巨算符类似 $\lim$或求和算符$\sum$，上下标位于上下方；后者令巨算符类似积分号，上下标位于右上方和右下方。  

行内：$\sum\limits_{i=1}^n \quad \int\limits_0^{\frac{\pi}{2}} \quad \prod\nolimits_\epsilon$

行间：

```latex
\sum\limits_{i=1}^n \quad \int\limits_0^{\frac{\pi}{2}} \quad \prod\nolimits_\epsilon
```

$$
\sum\limits_{i=1}^n \quad \int\limits_0^{\frac{\pi}{2}} \quad \prod\nolimits_\epsilon
$$
​	amsmath 宏包还提供了 `\substack`，能够在下限位置书写多行表达式； subarray 环境更进一步，令多行表达式可选择居中 (c) 或左对齐 (l)：  

```latex
\sum_{\substack{0\le i\le n \\
j\in \mathbb{R}}}
P(i, j) = Q{n} \\

\sum_{\begin{subarray}{l}
	0\le i \le n \\
	j \in \mathbb{R}
\end{subarray}}
P(i,j) = Q{n}\\

// 右对齐网页无法显示，typora可以正常显示
\sum_{\begin{subarray}{r}
	0\le i \le n \\
	j \in \mathbb{R}
\end{subarray}}
P(i,j) = Q{n}
```

$$
\sum_{\substack{0\le i\le n \\
j\in \mathbb{R}}}
P(i, j) = Q{n} \\

\sum_{\begin{subarray}{l}
	0\le i \le n \\
	j \in \mathbb{R}
\end{subarray}}
P(i,j) = Q{n}\\

$$

### 2.7 数学重音和上下括号

​	数学符号可以像文字一样加重音，比如求导符号 $\dot{r}$(`\dot{r}`)、 $\ddot{r}$(`\ddot{r}`)、表示向量的箭头 $\vec{r}$ (`\vec{r}`) 、表示单位向量的符号 $\hat{\mathbf{e}}$(`\hat{\mathbf{e}}`) 等，详见表 。使用时要注意重音符号的作用区域，一般应当对某个符号而不是“符号加下标”使用重音：  

```latex
\bar{x_0} \quad \bar{x}_0 \\
\vec{x_0} \quad \vec{x}_0 \\
\hat{\mathbf{e}_x} \quad \hat{\mathbf{e}}_x
```

$$
\bar{x_0} \quad \bar{x}_0 \\
\vec{x_0} \quad \vec{x}_0 \\
\hat{\mathbf{e}_x} \quad \hat{\mathbf{e}}_x
$$

​	LATEX 也能为多个字符加重音，包括直接画线的`\overline` 和 `\underline` 命令（可叠加使用）、宽重音符号 `\widehat`、表示向量的箭头 `\overrightarrow` 等。后两者详见表 。  

```latex
0.\overline{3} =
\underline{\underline{1/3}} \\
\widehat{XY} \qquad \overrightarrow{AB}\\
//下面的网页端无法正常显示，typora可以
$\hat{XY} \qquad $\vec{AB} \\
```

$$
0.\overline{3} =
\underline{\underline{1/3}} \\
\widehat{XY} \qquad \overrightarrow{AB}
$$
`\overbrace` 和 `\underbrace` 命令用来生成上/下括号，各自可带一个上/下标公式。  

```latex
\underbrace{\overbrace{(a+b+c)}^6
\cdot \overbrace{(d+e+f)}^7
_\text{meaning of file}} = 42
```

$$
\underbrace{\overbrace{(a+b+c)}^6
\cdot \overbrace{(d+e+f)}^7
_\text{meaning of file}} = 42
$$


### 2.8 箭头

​	常用的箭头包括` \rightarrow` ($\to$，或 `\to`)、 `\leftarrow`（$\gets$，或 `\gets`）等。更多箭头详见表 。amsmath 的 `\xleftarrow` 和 `\xrightarrow `命令提供了长度可以伸展的箭头，并且可以为箭头增加上下标：  

```latex
a \xleftarrow{x+y+z} b \\
c \xrightarrow[x<y]{a*b*c} d
```


$$
a \xleftarrow{x+y+z} b \\
c \xrightarrow[x<y]{a*b*c} d
$$

### 2.9 括号和定界符

​	LATEX 提供了多种括号和定界符表示公式块的边界，如小括号$()$、中括号$[]$、大括号 $\{\}$（`\\{\\}`）、尖括号 $\langle \rangle$ （`\langle \rangle`）等。更多的括号/定界符命令见表。  

```latex
{a,b,c} \neq \{a,b,c\}
```

$$
{a,b,c} \neq \{a,b,c\}
$$
​	使用 `\left` 和 `\right` 命令可令括号（定界符）的大小可变，在行间公式中常用。 LATEX 会自动根据括号内的公式大小决定定界符大小。 `\left` 和 `\right` 必须成对使用。需要使用单个定界符时，另一个定界符写成 `\left.` 或 `\right.`。  

```latex
1 + \left( \frac{1}{1-x^{2}} \right)^3 \qquad
\left. \frac{\partial f}{\partial t} \right|_{t=0}
```


$$
1 + \left( \frac{1}{1-x^{2}} \right)^3 \qquad
\left. \frac{\partial f}{\partial t} \right|_{t=0}
$$
​	有时我们不满意于 LATEX 为我们自动调节的定界符大小。这时我们还可以用`\big`、 `\bigg`等命令生成固定大小的定界符。更常用的形式是类似 `\left` 的`\bigl`、 `\biggl` 等，以及类似`\right` 的 `\bigr`、 `\biggr` 等（`\bigl` 和` \bigr` 不必成对出现）。  

```latex
\Bigl((x+1)(x+2)\Bigr)^{2}
```

$$
\Bigl((x+1)(x+2)\Bigr)^{2}
$$

```latex
\bigl( \Bigl( \biggl( \Biggl( \quad
\bigr) \Bigr) \biggr) \Biggr) \quad
\big\| \Big\| \biggl\| \Biggl \| \quad
\big\Downarrow \Big\Downarrow \bigg\Downarrow \Bigg\Downarrow
```

$$
\bigl( \Bigl( \biggl( \Biggl( \quad
\bigr) \Bigr) \biggr) \Biggr) \quad
\big\| \Big\| \biggl\| \Biggl \| \quad
\big\Downarrow \Big\Downarrow \bigg\Downarrow \Bigg\Downarrow
$$

​	使用 `\big` 和 `\bigg` 等命令的另外一个好处是：用 `\left` 和 `\right` 分界符包裹的公式块是不允许断行的（下文提到的 `array` 或者 `aligned` 等环境视为一个公式块），所以也不允许在多行公式里跨行使用，而 `\big` 和 `\bigg` 等命令不受限制。  



## 3. 多行公式

### 3.1 长公式折行

​	通常来讲应当避免写出超过一行而需要折行的长公式。如果一定要折行的话，习惯上优先在等号之前折行，其次在加号、减号之前，再次在乘号、除号之前。其它位置应当避免折行。amsmath 宏包的 `multline` 环境提供了书写折行长公式的方便环境。它允许用 `\\` 折行，将公式编号放在最后一行。多行公式的首行左对齐，末行右对齐，其余行居中。

```latex
// 网页端无法正常显示，typora可以
\begin{multline}
a + b + c + d + e + f + g + h + i \\
= j + k + l + m + n\\
= o + p + q + r + s\\
= t + u + v + x + z
\end{multline}
```

$$
\begin{multline}
a + b + c + d + e + f + g + h + i \\
= j + k + l + m + n\\
= o + p + q + r + s\\
= t + u + v + x + z
\end{multline}
$$


### 3.2 多行公式

​	更多的情况是，我们需要罗列一系列公式，并令其按照等号对齐。  

​	目前最常用的是 `align` 环境，它将公式用 `&` 隔为两部分并对齐。分隔符通常放在等号左边：

```latex
\begin{aligned}
a & = b + c\\
 & = d + e
\end{aligned}
```

$$
\begin{aligned}
a & = b + c\\
 & = d + e
\end{aligned}
$$
`align` 还能够对齐多组公式，除等号前的 `&` 之外，公式之间也用 `&` 分隔：  

```latex
\begin{aligned}
a &=1 & b &=2 & c &=3 \\
d &=-1 & e &=-2 & f &=-5
\end{aligned}
```

$$
\begin{aligned}
a &=1 & b &=2 & c &=3 \\
d &=-1 & e &=-2 & f &=-5
\end{aligned}
$$
如果我们不需要按等号对齐，只需罗列数个公式， `gather` 将是一个很好用的环境：  

```latex
\begin{gathered}
a = b + c \\
d = e + f + g \\
h + i = j + k\\
l + m = n
\end{gathered}
```

$$
\begin{gathered}
a = b + c \\
d = e + f + g \\
h + i = j + k \\
l + m = n
\end{gathered}
$$
不用`gather`则行间距略大：

```latex
a = b + c \\
d = e + f + g \\
h + i = j + k \\
l + m = n
```


$$
a = b + c \\
d = e + f + g \\
h + i = j + k \\
l + m = n
$$

### 3.3 公式编号的多行公式

​	另一个常见的需求是将多个公式组在一起公用一个编号，编号位于公式的居中位置。为此，amsmath 宏包提供了诸如 `aligned`、 `gathered` 等环境，与 `equation `环境（可用`\tags`替代）套用。以 -ed 结尾的环境用法与前一节不以 -ed 结尾的环境用法一一对应。我们仅以 aligned 举例：  

```latex
\begin{aligned}
a &= b + c \\
d &= e + f + g \\
h + i &= j + k \\
l + m &= n
\end{aligned}
\tag{123}
```

$$
\begin{aligned}
a &= b + c \\
d &= e + f + g \\
h + i &= j + k \\
l + m &= n
\end{aligned}
\tag{123}
$$


## 4. 数组和矩阵

​	为了排版二维数组， LATEX 提供了 `array` 环境，用法与 tabular 环境极为类似，也需要定义列格式，并用 \\ 换行。数组可作为一个公式块，在外套用 `\left`、` \right` 等定界符：  

```latex
\mathbf{X} = \left(
\begin{array}{cccc}
x_{11} & x_{12} & \ldots & x_{1n}\\
x_{21} & x_{22} & \ldots & x_{2n}\\
\vdots & \vdots & \ddots & \vdots\\
x_{n1} & x_{n2} & \ldots & x_{nn}\\
\end{array} \right)
```

$$
\mathbf{X} = \left(
\begin{array}{cccc}
x_{11} & x_{12} & \ldots & x_{1n}\\
x_{21} & x_{22} & \ldots & x_{2n}\\
\vdots & \vdots & \ddots & \vdots\\
x_{n1} & x_{n2} & \ldots & x_{nn}\\
\end{array} \right)
$$
​	值得注意的是，上一节末尾介绍的 `aligned` 等环境也可以用定界符包裹。  

​	我们还可以利用空的定界符排版出这样的效果：  

```latex
|x| = \left\{
\begin{array}{rl}
-x & \text{if } x < 0,\\
0 & \text{if } x = 0,\\
x & \text{if } x > 0.
\end{array} \right.
```

$$
|x| = \left\{
\begin{array}{rl}
-x & \text{if } x < 0,\\
0 & \text{if } x = 0,\\
x & \text{if } x > 0.
\end{array} \right.
$$
不过上述例子可以用 amsmath 提供的 `cases` 环境更轻松地完成：  

```latex
|x| =
\begin{cases}
-x & \text{if } x < 0,\\
0 & \text{if } x = 0,\\
x & \text{if } x > 0.
\end{cases}
```

$$
|x| =
\begin{cases}
-x & \text{if } x < 0,\\
0 & \text{if } x = 0,\\
x & \text{if } x > 0.
\end{cases}
$$
​	我们当然也可以用 `array` 环境排版各种矩阵。 amsmath 宏包还直接提供了多种排版矩阵的环境，包括不带定界符的 matrix，以及带各种定界符的矩阵 `pmatrix`（$($）、 `bmatrix`（$[$）、 `Bmatrix`（$\{$）、 `vmatrix`（$|$）、 `Vmatrix`（$\|$）。使用这些环境时，无需给定列格式：  

```latex
\begin{matrix}
1 & 2 \\ 3 & 4
\end{matrix} \qquad
\begin{bmatrix}
x_{11} & x_{12} & \ldots & x_{1n}\\
x_{21} & x_{22} & \ldots & x_{2n}\\
\vdots & \vdots & \ddots & \vdots\\
x_{n1} & x_{n2} & \ldots & x_{nn}\\
\end{bmatrix}
```

$$
\begin{matrix}
1 & 2 \\ 3 & 4
\end{matrix} \qquad
\begin{bmatrix}
x_{11} & x_{12} & \ldots & x_{1n}\\
x_{21} & x_{22} & \ldots & x_{2n}\\
\vdots & \vdots & \ddots & \vdots\\
x_{n1} & x_{n2} & \ldots & x_{nn}\\
\end{bmatrix}
$$
​	在矩阵中的元素里排版分式时，一来要用到 `\dfrac` 等命令，二来行与行之间有可能紧贴着，这时要用到 `\\[8pt]` 的方法来调节间距：  

```latex
\mathbf{H}=
\begin{bmatrix}
\dfrac{\partial^2 f}{\partial x^2} &
\dfrac{\partial^2 f}
{\partial x \partial y} \\[8pt]
\dfrac{\partial^2 f}
{\partial x \partial y} &
\dfrac{\partial^2 f}{\partial y^2}
\end{bmatrix}
```

$$
\mathbf{H}=
\begin{bmatrix}
\dfrac{\partial^2 f}{\partial x^2} &
\dfrac{\partial^2 f}
{\partial x \partial y} \\[8pt]
\dfrac{\partial^2 f}
{\partial x \partial y} &
\dfrac{\partial^2 f}{\partial y^2}
\end{bmatrix}
$$

## 5. 公式中的间距

​	前文提到过，绝大部分时候，数学公式中各元素的间距是根据符号类型自动生成的，需要我们手动调整的情况极少。我们已经认识了两个生成间距的命令 `\quad` 和 `\qquad`。在公式中我们还可能用到的间距包括 `\,`、 `\:`、 `\;` 以及负间距 `\!`，其中 `\quad` 、 `\qquad` 和 `\,` 在文本和数学环境中可用，后三个命令只用于数学环境。

```latex
\begin{aligned}
&aa \\
&a \quad b \\
&a \qquad b\\
&a \ a \\
&a \, a\\
&a \: a \\
&a \; a \\
&a \! a
\end{aligned}
```

$$
\begin{aligned}
&aa \\
&a \quad b \\
&a \qquad b\\
&a \ a \\
&a \, a\\
&a \: a \\
&a \; a \\
&a \! a
\end{aligned}
$$
​	一个常见的用途是修正积分的被积函数 f(x) 和微元 dx 之间的距离。注意微元里的 d 用的是直立体：  

```latex
\int_a^b f(x)\mathrm{d}x
\qquad
\int_a^b f(x)\,\mathrm{d}x
```

$$
\int_a^b f(x)\mathrm{d}x
\qquad
\int_a^b f(x)\,\mathrm{d}x
$$
​	另一个用途是生成多重积分号。如果我们直接连写两个 `\int`，之间的间距将会过宽，此时可以使用负间距 `\!` 修正之。不过 amsmath 提供了更方便的多重积分号，如二重积分 `\iint`、三重积分 `\iiint` 等`\newcommand\diff{\,\mathrm{d}}`相当于C语言宏。

```latex
\newcommand\diff{\,\mathrm{d}}

\begin{gathered}
\int\int f(x)g(y)
\diff x \diff y \\
\int\!\!\!\int
f(x)g(y) \diff x \diff y \\
\iint f(x)g(y) \diff x \diff y \\
\iint\quad \iiint\quad \idotsint
\end{gathered}
```

$$
\newcommand\diff{\,\mathrm{d}}

\begin{gathered}
\int\int f(x)g(y)
\diff x \diff y \\
\int\!\!\!\int
f(x)g(y) \diff x \diff y \\
\iint f(x)g(y) \diff x \diff y \\
\iint\quad \iiint\quad \idotsint
\end{gathered}
$$

## 6. 数学符号的字体控制

### 6.1 数学字母字体

### 6.2 数学符号的尺寸

​	数学符号按照符号排版的位置规定尺寸，从大到小包括行间公式尺寸、行内公式尺寸、上下标尺寸、次级上下标尺寸。除了字号有别之外，行间和行内公式尺寸下的巨算符也使用不一样的大小。 LATEX 为每个数学尺寸指定了一个切换的命令。 

<center><b>数字字母字体</b></center>

| 示例                          | 命令             |
| :---------------------------- | ---------------- |
| $\mathnormal{ABCDEabcde1234}$ | \mathnormal{...} |
| $\mathrm{ABCDEabcde1234}$     | **\mathrm{…}**   |
| $\mathit{ABCDEabcde1234}$     | \mathit{…}       |
| $\mathbf{ABCDEabcde1234}$     | **\mathbf{…}**   |
| $\mathsf{ABCDEabcde1234}$     | \mathsf{…}       |
| $\mathtt{ABCDEabcde1234}$     | \mathtt{…}       |
| $\mathcal{ABCDEabcde1234}$    | \mathcal{…}      |
| $\mathscr{ABCDEabcde1234}$    | \mathscr{…}      |
| $\mathfrak{ABCDEabcde1234}$   | \mathfrak{...}   |
| $\mathbb{ABCDEabcde1234}$     | \mathbb{...}     |

<center><b>数字符号尺寸</b></center>

| 命令               | 尺寸           | 示例                   |
| ------------------ | -------------- | ---------------------- |
| \displaystyle      | 行间公式尺寸   | $\displaystyle \sum a$ |
| \textstyle         | 行内公式尺寸   | $\textstyle \sum a$    |
| \scriptstyle       | 上下标尺寸     | $\scriptstyle a$       |
| \scriptscriptstyle | 次级上下标尺寸 | $\scriptscriptstyle a$ |

​	我们通过以下示例对比行间公式和行内公式的区别。在分式中，分子分母默认为行内公式尺寸，示例中将分母切换到行间公式尺寸：  

```latex
r = \frac
{\sum_{i=1}^n (x_i- x)(y_i- y)}
{\displaystyle \left[
\sum_{i=1}^n (x_i-x)^2
\sum_{i=1}^n (y_i-y)^2
\right]^{1/2} }
```

$$
r = \frac
{\sum_{i=1}^n (x_i- x)(y_i- y)}
{\displaystyle \left[
\sum_{i=1}^n (x_i-x)^2
\sum_{i=1}^n (y_i-y)^2
\right]^{1/2} }
$$

### 6.3 加粗的数学符号

​	在 LATEX 中为符号切换数学字体并不十分自由，只能通过 `\mathbf` 等有限的命令切换字体。比如想得到粗斜体的符号，就没有现成的命令；再比如 `\mathbf` 只能改变拉丁字母和大写希腊字母，小写希腊字母就没有用。
LATEX 提供了一个命令 `\boldmath` 令用户可以将整套数学字体切换为粗体版本（前提是数学字体宏包本身支持粗体符号）。但这个命令只能在公式外使用：  

```latex
\mu, M \qquad
\boldsymbol{\mu}, \boldsymbol{M}
```

$$
\mu, M \qquad
\boldsymbol{\mu}, \boldsymbol{M}
$$






## 7. 模板

---

```latex
\left(x-1\right)\left(x+3\right)
```

$$
\left(x-1\right)\left(x+3\right)
$$

---

```latex
\sqrt{a^2+b^2}
```

$$
\sqrt{a^2+b^2}
$$

---

```latex
\left ( \frac{a}{b}\right )^{n}= \frac{a^{n}}{b^{n}}
```

$$
\left ( \frac{a}{b}\right )^{n}= \frac{a^{n}}{b^{n}}
$$

---

```latex
x ={-b \pm \sqrt{b^2-4ac}\over 2a}
```

$$
x ={-b \pm \sqrt{b^2-4ac}\over 2a}
$$

---

```latex
a > b,b > c \Rightarrow a > c
```

$$
a > b,b > c \Rightarrow a > c
$$

---

```latex
\int \frac{1}{1+x^{2}}\mathrm{d}x= \arctan x +C
```

$$
\int \frac{1}{1+x^{2}}\mathrm{d}x= \arctan x +C
$$

---

```latex
f(x) = \int_{-\infty}^\infty  \hat f(x)\xi\,e^{2 \pi i \xi x}  \,\mathrm{d}\xi
```

$$
f(x) = \int_{-\infty}^\infty  \hat f(x)\xi\,e^{2 \pi i \xi x}  \,\mathrm{d}\xi
$$

---

```latex
\begin{pmatrix}  
  a_{11} & a_{12} & a_{13} \\  
  a_{21} & a_{22} & a_{23} \\  
  a_{31} & a_{32} & a_{33}  
\end{pmatrix}
```


$$
\begin{pmatrix}  
  a_{11} & a_{12} & a_{13} \\  
  a_{21} & a_{22} & a_{23} \\  
  a_{31} & a_{32} & a_{33}  
\end{pmatrix}
$$

---

```latex
\begin{pmatrix}  
  a_{11} & \cdots & a_{1n} \\  
  \vdots & \ddots & \vdots \\  
  a_{m1} & \cdots & a_{mn}  
\end{pmatrix}
```

$$
\begin{pmatrix}  
  a_{11} & \cdots & a_{1n} \\  
  \vdots & \ddots & \vdots \\  
  a_{m1} & \cdots & a_{mn}  
\end{pmatrix}
$$

---

```latex
\mathbf{A}_{m\times n}=  
\begin{bmatrix}  
  a_{11}& a_{12}& \cdots  & a_{1n} \\  
  a_{21}& a_{22}& \cdots  & a_{2n} \\  
  \vdots & \vdots & \ddots & \vdots \\  
  a_{m1}& a_{m2}& \cdots  & a_{mn}  
\end{bmatrix}  
=\left [ a_{ij}\right ]
```

$$
\mathbf{A}_{m\times n}=  
\begin{bmatrix}  
  a_{11}& a_{12}& \cdots  & a_{1n} \\  
  a_{21}& a_{22}& \cdots  & a_{2n} \\  
  \vdots & \vdots & \ddots & \vdots \\  
  a_{m1}& a_{m2}& \cdots  & a_{mn}  
\end{bmatrix}  
=\left [ a_{ij}\right ]
$$

---

```latex
X_1, \cdots,X_n
```

$$
X_1, \cdots,X_n
$$

---

```latex
\frac{\sin A}{a}=\frac{\sin B}{b}=\frac{\sin C}{c}=\frac{1}{2R}
```

$$
\frac{\sin A}{a}=\frac{\sin B}{b}=\frac{\sin C}{c}=\frac{1}{2R}
$$

---

```latex
\begin{array}{c} 
  \text{若}P \left( AB \right) =P \left( A \right) P \left( B \right) \\  
  \text{则}P \left( A \left| B\right. \right) =P \left({B}\right) 
\end{array}
```

$$
\begin{array}{c} 
  \text{若}P \left( AB \right) =P \left( A \right) P \left( B \right) \\  
  \text{则}P \left( A \left| B\right. \right) =P \left({B}\right) 
\end{array}
$$

---

```latex
(1+x)^{n} =1 + \frac{nx}{1!} + \frac{n(n-1)x^{2}}{2!} + \cdots
```

$$
(1+x)^{n} =1 + \frac{nx}{1!} + \frac{n(n-1)x^{2}}{2!} + \cdots
$$

---

```latex
\lambda 
= \frac{\displaystyle{\frac{c^2}{v}}}
	   {\displaystyle{\frac{m c^2}{h}}}
= \frac{h}{mv} 
= \frac{h}{p}
```

$$
\lambda 
= \frac{\displaystyle{\frac{c^2}{v}}}
	   {\displaystyle{\frac{m c^2}{h}}}
= \frac{h}{mv} 
= \frac{h}{p}
$$



