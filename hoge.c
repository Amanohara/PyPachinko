#include <stdio.h>
 
int main(void) {
  while(1){
    printf(" -\r");
    usleep(100000);
    fflush(stdout);
    printf(" \\\r");
    usleep(100000);
    fflush(stdout);
    printf(" |\r");
    usleep(100000);
    fflush(stdout);
    printf(" /\r");
    usleep(100000);
    fflush(stdout);
  }
}
