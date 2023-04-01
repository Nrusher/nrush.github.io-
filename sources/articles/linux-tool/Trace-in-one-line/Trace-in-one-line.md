---
layout: default
title: Trace in one line
categories: linux-tool
author: Nrush
create_time: 2023-04-01 20:47:45
---
<center><h1>{{page.title}}</h1></center>

```sh
# enable/disable trace out
echo 1 > /sys/kernel/debug/tracing/tracing_on
echo 0 > /sys/kernel/debug/tracing/tracing_on

# read trace buffer log
cat /sys/kernel/debug/tracing/trace

# clear trace buffer
echo > /sys/kernel/debug/tracing/trace

# enable a TRACE_EVENT
echo 1 > /sys/kernel/debug/tracing/events/xxx/xxx/enable
```