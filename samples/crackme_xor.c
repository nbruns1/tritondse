
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *serial = "\x31\x3e\x3d\x26\x31";

int check(char *ptr)
{
  int i = 0;

  while (i < 5){
    if (((ptr[i] - 1) ^ 0x55) != serial[i])
      return 1;
    i++;
  }
  return 0;
}

int main(int ac, char **av)
{
  int ret;
  char buff[32];

  read(0, buff, sizeof(buff) - 1);

  ret = check(buff);
  if (ret == 0)
    printf("Win\n");
  else
    printf("fail\n");

  return 0;
}

