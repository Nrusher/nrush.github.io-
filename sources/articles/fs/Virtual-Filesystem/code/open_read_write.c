#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(void) {
    int fd = 0;
    char buf[128];
    size_t len = 0;

    remove("./test.txt");
    creat("./test.txt", 0777);
    fd = open("./test.txt", O_RDWR, 0777);

    len = sizeof("hello fs");
    len = write(fd, "hello fs", len);
    printf("wr len:%lu, str: %s\n", len, "hello fs");

    lseek(fd, 0, SEEK_SET);

    len = read(fd, buf, sizeof(buf));
    buf[len] = '\0';
    printf("rd len:%lu, str: %s\n", len, buf);

    close(fd);
    remove("./test.txt");
    return 0;
}