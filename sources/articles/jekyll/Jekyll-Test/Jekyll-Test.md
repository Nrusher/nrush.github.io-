---
layout: default
title:  "Jekyll Test"
create_time:   2023-02-28 00:34:13
categories: jekyll
author: Nrush
---

<strong>Table of Contents</strong>
- this unordered seed list will be replaced by toc as unordered list
{:toc}

I have been play with jekyll for a week. And this is my First jekyll blog. Best wish to my blog website! &#128420;

## 1 Text

### 1.1  中文
这个博客用来测试jekyll的特性。

### 1.2  English
This blog is used to test jekyll's features. 

### 1.3  blockquotes
> hello

### 1.4 emoji
<http://www.unicode.org/charts/>必须是10进制数
&copy;
&#2665;
&#128420;

## 2 Code
```c
#include <stdio.h>
int main(void) {
    printf("hello world");
}
```

```sh
echo hello world!
```

```python
import os

print("hello world!")
```

## 3 Math
```math
a + b
```

$$
\begin{align*}
  & \phi(x,y) = \phi \left(\sum_{i=1}^n x_ie_i, \sum_{j=1}^n y_je_j \right)
  = \sum_{i=1}^n \sum_{j=1}^n x_i y_j \phi(e_i, e_j) = \\
  & (x_1, \ldots, x_n) \left( \begin{array}{ccc}
      \phi(e_1, e_1) & \cdots & \phi(e_1, e_n) \\
      \vdots & \ddots & \vdots \\
      \phi(e_n, e_1) & \cdots & \phi(e_n, e_n)
    \end{array} \right)
  \left( \begin{array}{c}
      y_1 \\
      \vdots \\
      y_n
    \end{array} \right)
\end{align*}
$$

$$ A + B $$

## 4 Image

<center><img src="/sources/images/test.jpg" alt="test_img" width=650/></center>

## 5 Video
<center>
<video width="320" height="240" controls>
  <source src="https://www.runoob.com/try/demo_source/movie.mp4"  type="video/mp4">
  <source src="https://www.runoob.com/try/demo_source/movie.mp4"  type="video/ogg">
  您的浏览器不支持 HTML5 video 标签。
</video>
</center>

## 6 url
<a href="{{ site.baseurl }}Jekyll-Test">Jekyll Test</a>

## 7 download
<a href="/sources/images/test.jpg" download="test.jpg">点击下载</a>

## Pdf Viewer

<center><embed src="/sources//pdf/devicetree-specification-v0.3-rc2.pdf" width="750px" height="1500px"></center>


