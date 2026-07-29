#include <stdio.h>

int main(int argc, char ** argv)
{
    for(int i =0; i<argc; i++) {
        printf("전달된 개수: %d\n", argc);
        if(argc >= 2)
        {
            printf("제품명 : ");
            for(int i=1; i<argc; i++){
                printf("%s ", argv[i]);
            }
    
         }
    }       
    printf("\n");
    return 0;

}