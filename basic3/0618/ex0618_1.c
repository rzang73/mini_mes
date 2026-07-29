#include <stdio.h>

// 함수 선언 (매개변수로 int형 배열 또는 포인터를 받음)
void print_max(int arr[]); 

int main()
{
    int array[7] = { 4, 5, 8, 1, 2, 3, 7 };
  
    // 함수 호출 (배열의 이름을 넣으면 배열의 첫 번째 요소 주소가 전달됩니다)
    print_max(array); 
   
    return 0;
}
// 가장 큰 값을 출력하는 함수 구현
void print_max(int arr[])
{
    // 1. 배열의 첫 번째 요소를 초기 최댓값으로 설정
    int max = arr[0]; 
    
    // 2. 반복문을 돌며 배열의 1번 인덱스부터 6번 인덱스까지 비교
    for (int i = 1; i < 7; i++)
    {
        if (arr[i] > max)
        {
            max = arr[i]; // 더 큰 값을 찾으면 max를 갱신
        }
    }
    
    // 3. 요구사항에 맞는 형식으로 출력
    printf("가장 큰 값 : %d\n", max);
}