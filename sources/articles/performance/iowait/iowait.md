---
layout: default
title: iowait
categories: performance
author: Nrush
create_time: 2023-04-01 20:44:58
---
<center><strong><font size=6>{{page.title}}</font></strong></center>

- this unordered seed list will be replaced by toc as unordered list
{:toc}

## 1 定义

`man sar`可以看到iowait的定义

```
Percentage of time that the CPU or CPUs were idle during which the system  had  an  out‐standing disk I/O request.
```

## 2 计算原理

iowait是cpu idle情况下等io所消耗时间占的百分比。**<u>iowait高不代表系统一定存在io性能瓶颈，iowait低也不一定代表系统没有io性能瓶颈, 这个指标仅仅反应的是cpu的一种空闲状态</u>**。

<center>
<table width="90%">
    <tbody align=center>
        <tr>
            <td><img src="/sources/images/iowait-20.svg" width=350></td>
            <td><img src="/sources/images/iowait-40.svg" width=350></td>
        </tr>
        <tr>
            <td>(1) iowait-20%</td>
            <td>(2) iowait-40%</td>
        </tr>
    </tbody>
</table>
</center>

如上图(1)、(2)所示系统的IO压力并未变化，但iowait却高了一倍。


## 3 实际使用

如果出现iowait高的情况，还是有必要去确认一下系统的io是否正常的，因为IO阻塞导致系统挂起线程过多，进而表现为iowait高的情况是存在的。总结下来这并不是一个十分可信的值。

```
iowait (since Linux 2.5.41)
      (5) Time waiting for I/O to complete.  This
      value is not reliable, for the following
      reasons:
       1. The CPU will not wait for I/O to
         complete; iowait is the time that a task
         is waiting for I/O to complete.  When a
         CPU goes into idle state for outstanding
         task I/O, another task will be scheduled
         on this CPU.
       2. On a multi-core CPU, the task waiting for
         I/O to complete is not running on any
         CPU, so the iowait of each CPU is
         difficult to calculate.
       3. The value in this field may decrease in
         certain conditions.
```
遇到iowait偏高是需要借助`sar -d 1`等工具，查看await、aqu-sz、util等io指标进一步确认是否的确存在io问题。
```
    DEV       tps     rkB/s     wkB/s     dkB/s   areq-sz    aqu-sz     await     %util
  loop0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
  loop1      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
  loop2      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
  loop3      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
  loop4      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
mmcblk0      1.59      0.13      9.54      1.04      6.73      0.02     12.61      0.42
```