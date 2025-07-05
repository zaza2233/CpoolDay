#include "print_char.h"
#include <stdlib.h>
void my_print_n_ascii(int n)
{
    if (n<=33 ||n>127)
    {
        exit(EXIT_SUCCESS);
    }
   for (int i=33;i<127;++i)
   {
        print_char(i);
   }
}
