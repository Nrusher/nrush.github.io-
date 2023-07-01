#include <stdio.h>
#include <time.h>

#define KB 1024
#define MB 1024 * 1024

int main() {
   long start, stop;
   int lengthMod = 8 * MB - 1;
   double totalTime, timeTaken;
   int tmp;
   double avg;

   static int array[8 * MB];                       // 开了8MB的数组作为操作对象
   int i, j;
   unsigned int k;
   /* Change the step of array iteration and observe the change in time taken for computation.
      The step('i' value) at which there is a significant change in time taken will correspond 
      to the cache line size */
   for (i = 1; i <= 2048; i *= 2) {              // 最外层循环，i会以2的倍数取值，例如1,2,4,8
      totalTime = 0;
      for (j = 0; j < 6; j++) {                  // 每个测试重复6次
         start = clock();
         for (k = 0; k < 512 * MB; k++) {        // 每次测试进行512M的操作，大约5亿次
            tmp += array[(k * i) & lengthMod];   // 下标对8MB取余，保证下标不溢出
         }
         timeTaken = (double)(clock() - start) / CLOCKS_PER_SEC;
         totalTime += timeTaken;
      }
      totalTime /= 6;                            // 取6次测试平均时间，作为结果
      printf("For i value: %d    Time Taken:%lf\n",i,totalTime);
   } 
}