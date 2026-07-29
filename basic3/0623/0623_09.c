#include <stdio.h>

struct address
{
    char name[20];
    int age;
    char tel[20];
    char addr[80];

};

void print_list(struct address *lp);

int main()
{
    struct address list[5] ={
        {"홍길동",23,"111-1111", "울릉도 독도"},
        {"이순신",30,"222-1111", "경상도 오지"},
        {"이성계",35,"333-1111", "전라도 외진"},
        {"김알지",45,"444-1111", "충청도 계란"},
        {"고조선",55,"555-1111", "강원도 외란"}
    };
    
    print_list(list);

    return 0;
}
void print_list(struct address*lp)
{
    int i;

    for( i =0; i< 5;i++)
    {
        printf("%10s%7d%15s%20s\n",
            (lp+i)->name, (lp+i)->age,(lp+i)->tel,(lp+i)->addr);

    }

}
