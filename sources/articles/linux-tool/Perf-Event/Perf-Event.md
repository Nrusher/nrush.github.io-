---
layout: default
title: Perf Event
categories: linux-tool
author: Nrush
create_time: 2023-04-01 20:51:43
---
<center><strong><font size=6>{{page.title}}</font></strong></center>

- this unordered seed list will be replaced by toc as unordered list
{:toc}

判断是否支持PMU，看启动log中又没有PMU关键字
```
cat /var/log/dmesg | grep PMU
```

https://blog.csdn.net/pwl999/article/details/81200439

使用perf采集系统调用栈的demo：<a href="/sources/demo/perf_event/perf_event_sample.c" download="perf_event_sample.c">perf_event_sample.c</a>




