#include <stdio.h>
#include <linux/perf_event.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <stdint.h>
#include <string.h>
#include <string.h>
#include <sys/mman.h>
#include <poll.h>
#include <sys/ioctl.h>

static int perf_event_open(struct perf_event_attr *evt_attr, pid_t pid, int cpu, int group_fd, unsigned long flags)
{
    int ret;
    ret = syscall(__NR_perf_event_open, evt_attr, pid, cpu, group_fd, flags);
    return ret;
}

struct perf_event_sample
{
    struct perf_event_header header;
    uint32_t    pid, tid;
    uint64_t    time;
    uint32_t    cpu, res;
    uint64_t    nr;
    uint64_t    ips[];
};

int main(void)
{
    int i = 0;
    int ret = 0;
    int fd = 0;
    /* must be 1 + 2^n */
    int buffer_size = (1 + 8) * 4096;
    void *buffer;
    struct perf_event_attr attr;

    memset(&attr, 0, sizeof(attr));
    attr.type = PERF_TYPE_SOFTWARE;
    attr.size = sizeof(attr);
    attr.config = PERF_COUNT_SW_CPU_CLOCK;
    attr.sample_period = 20000000;
    attr.wakeup_events = 1;
    attr.sample_type = PERF_SAMPLE_CALLCHAIN | PERF_SAMPLE_CPU | PERF_SAMPLE_TIME | PERF_SAMPLE_TID;
    attr.disabled = 1;

    fd = perf_event_open(&attr, -1, 0, -1, 0);
    if (fd < 0) {
        printf("perf_event_open failed %d\n", fd);
        return -1;
    }

    /* prot should be PORT_READ, flags should be MAP_SHAED */
    buffer = mmap(NULL, buffer_size, PROT_READ, MAP_SHARED, fd, 0);
    if (buffer == MAP_FAILED) {
        printf("mmap failed! %p\n", buffer);
        return -1;
    }

    struct pollfd pfd = {
        .fd = fd,
        .events = POLLIN};

    struct perf_event_sample *sample;
    struct perf_event_mmap_page *info = buffer;
    uint64_t last_offset = 0;
    uint8_t *data_base = (uint8_t *)info + 4096;
    uint8_t *data_start = 0;

    ioctl(fd, PERF_EVENT_IOC_RESET, 0);
    ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);

    printf("start sample ....\n");

    while (1) {
        ret = poll(&pfd, 1, -1);
        if (ret == -1) {
            printf("poll failed!\n");
            return -1;
        }

        printf("sample: \n");
        sample = (struct perf_event_sample *)(data_base + last_offset);
        if (sample->header.type != PERF_RECORD_SAMPLE)
            continue;

        printf("time:%lu, pid: %u, tid: %u, cpu: %u\n", sample->time,
                                                           sample->pid,
                                                           sample->tid,
                                                           sample->cpu);
        for (i = 0; i < sample->nr; i++)
            printf("[%d] 0x%lx\n", i, sample->ips[i]);
        
        last_offset = info->data_head;
    }

    close(fd);
    munmap(buffer, buffer_size);
}