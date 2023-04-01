---
layout: default
title: Trace Point
categories: linux-tool
author: Nrush
create_time: 2023-04-01 20:47:07
---
<center><h1>{{page.title}}</h1></center>

trace_xxx在Linux内核中随处可见，从目的上看，这些代码和debug时加入的printk调试代码没有区别，都是采集输出代码上下文信息，以便于分析性能和稳定性问题。和简单粗暴的printk以及自定义的debug函数相比，tracepoint机制提供了一种更为优雅、便捷和强大的静态调试点插入方式。

## 1. 如何使用tracepoint

在了解tracepoint实现前，先看一下linux tracepoint和用户的交互机制。所有tracepoint的输出都被存放在trace的ringbuffer中，想要查看这些输出，只需要`cat /sys/kernel/debug/tracing/trace`目录即可。当然只有打开特定tracepoint的开关后对应tracepoint才会生效并输出数据。一个完整的使用例子如下
```sh
# step 1 enable a Event
echo 1 > /sys/kernel/debug/tracing/events/sched/sched_process_fork/enable
# step 2 enable trace
echo 1 > /sys/kernel/debug/tracing/tracing_on
# step 3 read ringbuffer
cat > /sys/kernel/debug/tracing/trace
```
此时起一个新进程时，trace buffer中会有对应的输出
```sh
# tracer: nop
#
# entries-in-buffer/entries-written: 3/3   #P:4
#
#                                _-----=> irqs-off
#                               / _----=> need-resched
#                              | / _---=> hardirq/softirq
#                              || / _--=> preempt-depth
#                              ||| / _-=> migrate-disable
#                              |||| /     delay
#           TASK-PID     CPU#  |||||  TIMESTAMP  FUNCTION
#              | |         |   |||||     |         |
            bash-54642   [003] ..... 1130406.191897: sched_process_fork: comm=bash pid=54642 child_comm=bash child_pid=54710
            bash-54642   [002] ..... 1130408.504988: sched_process_fork: comm=bash pid=54642 child_comm=bash child_pid=54711
            bash-54642   [003] ..... 1130409.677837: sched_process_fork: comm=bash pid=54642 child_comm=bash child_pid=54712
```

更多trace的使用方式见：<a href="{{ site.baseurl }}Trace-in-oneline">Trace-in-oneline</a>

## 2. 实现原理

根据tracepoint的使用方法，不难想出其底层代码不外乎如下逻辑。
```c
trace_xxx(args) {
  if (enabled) {
    run_trace_function(arg)
  }
}
```
找一个trace函数（`trace_sched_wait_task(p)`）验证以上猜想。
```c
trace_sched_wait_task(p)
  --> [include/trace/events/sched.h]
      DEFINE_EVENT(sched_process_template, 
                   sched_wait_task,
                   TP_PROTO(struct task_struct *p),
                   TP_ARGS(p)); 
      
  --> [include/linux/tracepoint.h]
      #define DEFINE_EVENT(template, name, proto, args)           \
              DECLARE_TRACE(name, PARAMS(proto), PARAMS(args))
              [include/trace/events/sched.h]

  --> [include/linux/tracepoint.h]
      #define DECLARE_TRACE(name, proto, args)                    \
              __DECLARE_TRACE(name, PARAMS(proto), PARAMS(args),  \
                        cpu_online(raw_smp_processor_id()),       \
                        PARAMS(void *__data, proto))
```
展开__DECLARE_TRACE可得
```c
__DECLARE_TRACE(name = sched_wait_task,
                proto = struct task_struct *p,
                args = p,
                cond = cpu_online(raw_smp_processor_id()),
                data_proto = void *__data, struct task_struct *p)

extern int __traceiter_sched_wait_task(void *__data, struct task_struct *p);                      
DECLARE_STATIC_CALL(tp_func_sched_wait_task, __traceiter_sched_wait_task);
extern struct tracepoint __tracepoint_sched_wait_task;                   
static inline void trace_sched_wait_task(struct task_struct *p)                          
{
        if (static_key_false(&__tracepoint_sched_wait_task.key)) {        
                /* __DO_TRACE(sched_wait_task, p, cpu_online(raw_smp_processor_id()), 0); */
                int __maybe_unused __idx = 0;
                                             
                if (!(cpu_online(raw_smp_processor_id())))                 
                        return;              
                                             
                /* srcu can't be used from NMI */                       
                WARN_ON_ONCE(rcuidle && in_nmi());                      
 
                /* keep srcu and sched-rcu usage consistent */          
                preempt_disable_notrace();   
                                             
                /*                           
                 * For rcuidle callers, use srcu since sched-rcu        
                 * doesn't work from the idle path.                     
                 */                          
                if (rcuidle) {               
                        __idx = srcu_read_lock_notrace(&tracepoint_srcu);
                        ct_irq_enter_irqson();                          
                }                            
                                             
                /* __DO_TRACE_CALL(sched_wait_task, p); */                                      
                struct tracepoint_func *it_func_ptr;                    
                void *__data;                                           
                it_func_ptr = rcu_dereference_raw((&__tracepoint_sched_wait_task)->funcs); 
                if (it_func_ptr) {                                      
                        __data = (it_func_ptr)->data;                   
                        static_call(tp_func_sched_wait_task)(__data, p);      
                }                                                       
                  
                if (rcuidle) {
                        ct_irq_exit_irqson();
                        srcu_read_unlock_notrace(&tracepoint_srcu, __idx);
                }                            
                                            
                preempt_enable_notrace();    
        }                
        if (IS_ENABLED(CONFIG_LOCKDEP) && (cpu_online(raw_smp_processor_id()))) {             
                rcu_read_lock_sched_notrace();                  
                rcu_dereference_sched(__tracepoint_sched_wait_task.funcs);
                rcu_read_unlock_sched_notrace();                
        }
}

__DECLARE_TRACE_RCU(name, struct task_struct *p, p, cpu_online(raw_smp_processor_id()))
static inline int                                               
register_trace_sched_wait_task(void (*probe)(void *__data, struct task_struct *p), void *data)    
{
        return tracepoint_probe_register(&__tracepoint_sched_wait_task,  
                                        (void *)probe, data);   
}
static inline int                                               
register_trace_prio_sched_wait_task(void (*probe)(void *__data, struct task_struct *p), void *data,
                          int prio)                            
{
        return tracepoint_probe_register_prio(&__tracepoint_sched_wait_task, 
                                    (void *)probe, data, prio); 
}
static inline int                                               
unregister_trace_sched_wait_task(void (*probe)(void *__data, struct task_struct *p), void *data)  
{
        return tracepoint_probe_unregister(&__tracepoint_sched_wait_task,
                                        (void *)probe, data);   
}
static inline void                                              
check_trace_callback_type_sched_wait_task(void (*cb)(void *__data, struct task_struct *p))        
{
}
static inline bool                                              
trace_sched_wait_task_enabled(void)                                    
{
        return static_key_false(&__tracepoint_sched_wait_task.key);
}
```

从展开的结果看，其的确如之前推测，linux采用了如下格式来定义一个trace点
```c
static inline void trace_sched_wait_task(struct task_struct *p) {
  ....
  if (static_key_false(&__tracepoint_sched_wait_task.key)) {
      /* do trace */
      .....
  }
  ....
}
```

但还有一些疑问，展开后，部分函数和变量只有声明却没有定义,如
```c
extern int __traceiter_sched_wait_task(void *__data, struct task_struct *p);                      
extern struct tracepoint __tracepoint_sched_wait_task; 
```
`include/trace/events/sched.h`如何做到使用一个宏既完成了函数定义又完成了相关声明的呢？这里内核使用了一个非常有技巧的宏定义方法，让同一个宏`DEFINE_EVENT`在特殊文件中会被展开成两次不同的定义。

还是以`sched_wait_task`为例，在`kernel/sched/core.c`include
`trace/events/sched.h`时，其会在引用前额外定义`CREATE_TRACE_POINTS`，这就是展开两次的trick点。

```c
kernel/sched/core.c
-------------------------------------
#define CREATE_TRACE_POINTS
#include <linux/sched/rseq_api.h>
#include <trace/events/sched.h>
#undef CREATE_TRACE_POINTS
```

但编译器编译到上述的include时，会先根据按tracepoint.h中的定义将`DEFINE_EVENT`映射成`DECLARE_TRACE`宏，这相当于展开了tracepoint的声明部分。注意，其include了define_trace.h，且是在`_TRACE_SCHED_H`宏保护范围之外的，这一点非常重要。

```c
include/trace/events/sched.h
-------------------------------------------
#undef TRACE_SYSTEM
#define TRACE_SYSTEM sched 
#if !defined(_TRACE_SCHED_H) || defined(TRACE_HEADER_MULTI_READ)
#define _TRACE_SCHED_H

#include <linux/tracepoint.h>
...
DEFINE_EVENT(sched_process_template, 
                   sched_wait_task,
                   TP_PROTO(struct task_struct *p),
                   TP_ARGS(p));
...
#endif
#include <trace/define_trace.h> 
```

```c
include/linux/tracepoint.h
------------------------------------------------------------------------
...
#define DEFINE_TRACE_FN(_name, _reg, _unreg, proto, args)               \
         static const char __tpstrtab_##_name[]                          \
         __section("__tracepoints_strings") = #_name;                    \
         extern struct static_call_key STATIC_CALL_KEY(tp_func_##_name); \
         int __traceiter_##_name(void *__data, proto);                   \
         struct tracepoint __tracepoint_##_name  __used                  \
         __section("__tracepoints") = {                                  \
                 .name = __tpstrtab_##_name,                             \
                 .key = STATIC_KEY_INIT_FALSE,                           \
                 .static_call_key = &STATIC_CALL_KEY(tp_func_##_name),   \
                 .static_call_tramp = STATIC_CALL_TRAMP_ADDR(tp_func_##_name), \
                 .iterator = &__traceiter_##_name,                       \
                 .regfunc = _reg,                                        \
                 .unregfunc = _unreg,                                    \
                 .funcs = NULL };                                        \
         __TRACEPOINT_ENTRY(_name);                                      \
         int __traceiter_##_name(void *__data, proto)                    \
         {                                                               \
                 struct tracepoint_func *it_func_ptr;                    \
                 void *it_func;                                          \
                                                                         \
                 it_func_ptr =                                           \
                         rcu_dereference_raw((&__tracepoint_##_name)->funcs); \
                 if (it_func_ptr) {                                      \
                         do {                                            \
                                 it_func = READ_ONCE((it_func_ptr)->func); \                                                       
                                 __data = (it_func_ptr)->data;           \
                                 ((void(*)(void *, proto))(it_func))(__data, args); \
                         } while ((++it_func_ptr)->func);                \
                 }                                                       \
                 return 0;                                               \
         }                                                               \
         DEFINE_STATIC_CALL(tp_func_##_name, __traceiter_##_name);

#define DEFINE_TRACE(name, proto, args)         \
        DEFINE_TRACE_FN(name, NULL, NULL, PARAMS(proto), PARAMS(args));
...

#ifndef TRACE_EVENT
#define DEFINE_EVENT(template, name, proto, args)       \
        DECLARE_TRACE(name, PARAMS(proto), PARAMS(args))
#endif
...
```

在define_trace.h中，其会会先undef `DEFINE_EVENT`， 然后将其映射成`DEFINE_TRACE`，同时会再include一次`trace/events/sched.h`，这次include会将`trace/events/sched.h`中的`DEFINE_EVENT`按`DEFINE_TRACE`，既会生成变量的定义部分，这便完成了一个宏定义既声明又定义的操作。


```c
include/trace/define_trace.h
-------------------------------------------------------
#ifdef CREATE_TRACE_POINTS        
/* Prevent recursion */     
#undef CREATE_TRACE_POINTS
...

#undef DEFINE_EVENT
#define DEFINE_EVENT(template, name, proto, args) \
        DEFINE_TRACE(name, PARAMS(proto), PARAMS(args))

#define TRACE_HEADER_MULTI_READ
...
/* TRACE_INCLUDE(system) ===> #include <include/trace/events/system.h> */
#include TRACE_INCLUDE(TRACE_INCLUDE_FILE)
...
#undef TRACE_HEADER_MULTI_READ

#define CREATE_TRACE_POINTS
#endif
```

每个`trace/events/xx.h`在所有代码中只会有一次在include之前添加`CREATE_TRACE_POINTS`，其余引用按正常头文件引用，这意味着定义部分只会被展开一次，进而避免了重复定义的问题。

一个定义完成两件事这个trick的核心点就在于让一个头文件中的内容展开两次，且以不同的定义展开。这个trick虽然并不是tracepoint的核心点，但由于非常有趣，还是在这里记上一笔。

观察`__traceiter_xxx`宏函数展开，很容易发现，linux tracepoint执行的tracepoint函数并非是静态单一的，它是动态多个的。
```c
int __traceiter_##_name(void *__data, proto)                    \
{                                                               \
        struct tracepoint_func *it_func_ptr;                    \
        void *it_func;                                          \
                                                                \
        it_func_ptr =                                           \
                rcu_dereference_raw((&__tracepoint_##_name)->funcs); \
        if (it_func_ptr) {                                      \
                do {                                            \
                        it_func = READ_ONCE((it_func_ptr)->func); \                                                       
                        __data = (it_func_ptr)->data;           \
                        ((void(*)(void *, proto))(it_func))(__data, args); \
                } while ((++it_func_ptr)->func);                \
        }                                                       \
        return 0;                                               \
}                                                               \
```
如何做到动态多个呢？`funcs`是一个函数指针数组，理论上可以指向任意一组需要执行的函数。这一点非常重要，这使得tracepoint可以作为bpf、ftrace等各种linux的调试跟踪机制的事件源。

## 3 总结

tracepoint与传统printk加debug log的静态调试点的比较
优势
- 代码集中规范，便于代码管理。
- 用户态可以灵活控制tracepoint是否生效。
- trace函数动态可配，便于满足不同trace的需求。

劣势
- 需要额外占用一部份内存