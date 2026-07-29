#include <stdio.h>
#include <stdlib.h>

#define WIDTH 640
#define HEIGHT 480
#define FRAMES 30 // 총 30프레임 (동영상 길이)

// 픽셀 구조체 정의
typedef struct {
    unsigned char r, g, b;
} Pixel;

// 2차원 영상 화면을 위한 배열 (실제로는 동적 할당이나 전역 변수 권장)
Pixel screen[HEIGHT][WIDTH];

int main() {
    char filename[50];

    for (int f = 0; f < FRAMES; f++) {
        // 1. 배열에 그라데이션 및 프레임 변화 데이터 채우기
        for (int y = 0; y < HEIGHT; y++) {
            for (int x = 0; x < WIDTH; x++) {
                screen[y][x].r = (x + f * 8) % 256; // 프레임(시간)이 흐를수록 빨간색이 움직임
                screen[y][x].g = y % 256;
                screen[y][x].b = 128;
            }
        }

        // 2. 배열 데이터를 PPM 이미지 파일로 저장
        sprintf(filename, "frame_%03d.ppm", f);
        FILE *fp = fopen(filename, "wb");
        
        // PPM 파일 헤더 작성
        fprintf(fp, "P6\n%d %d\n255\n", WIDTH, HEIGHT);
        
        // 배열 데이터 통째로 파일에 쓰기
        fwrite(screen, sizeof(Pixel), WIDTH * HEIGHT, fp);
        fclose(fp);
    }

    printf("%d개의 프레임 이미지 생성 완료!\n", FRAMES);
    return 0;
}