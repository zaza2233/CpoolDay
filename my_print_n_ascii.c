#include "print_char.h"
#include <stdlib.h>
void my_print_n_ascii(int n)
{
    if (n<=0 ||n>94)
    {
        return;
    }
    n=n+33;
   for (int i=33; i<0;i++)
   {
        print_char(i);
   }
}
