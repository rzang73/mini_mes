#include <stdio.h>

// 단어들을 'AAA'부터 출력하고, 총 개수를 반환하는 함수
int printCombinations(char *wordPtr) 
{
    int count = 0; 

    // 첫 번째 글자 'A'부터 'Z'까지
    for (char i = 'A'; i <= 'Z'; i++) 
    {
        // 두 번째 글자 'A'부터 'Z'까지
        for (char j = 'A'; j <= 'Z'; j++) 
        {
            // 세 번째 글자 'A'부터 'Z'까지
            for (char k = 'A'; k <= 'Z'; k++) 
            {
                // 포인터를 활용해 문자 배열에 글자 세팅
                *(wordPtr + 0) = i; 
                *(wordPtr + 1) = j; 
                *(wordPtr + 2) = k; 

                // 단어 출력 후 공백 한 칸
                printf("%s ", wordPtr);
                count++;

                // 10단어마다 줄바꿈
                if (count % 10 == 0) 
                {
                    printf("\n");
                }
            }
        }
    }

    return count;
}

int main() 
{
    char word[4] = {0, }; 
    word[3] = '\0'; // 문자열 끝 지정

    // 함수 호출 (AAA부터 시작)
    int totalCount = printCombinations(word);

    // 최종 결과 출력
    printf("\n총 단어의 수는 : %d개\n", totalCount);

    return 0;
}