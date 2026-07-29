#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>

// 5M 및 4-1) 자격관리를 반영한 구조체
typedef struct {
    int emp_id;
    char name[20];
    char department[30];
    int is_present;
    char qualification[30]; 
} Employee;

// 함수 프로토타입 선언
void init_database(sqlite3 **db);
void run_integrated_mes_menu(sqlite3 *db);
void register_employee(sqlite3 *db);
void check_in_employee(sqlite3 *db);
void view_present_employees(sqlite3 *db);
void view_absent_employees(sqlite3 *db);
void view_all_employees(sqlite3 *db);

int main() {
    sqlite3 *db = NULL;
    init_database(&db); 

    // 실행 즉시 전체 메뉴 대시보드가 화면에 뜨도록 호출
    run_integrated_mes_menu(db);

    sqlite3_close(db);
    printf("MES 프로그램을 안전하게 종료합니다.\n");
    return 0;
}

// 데이터베이스 초기화 및 테이블 분리 (정규화 설계)
void init_database(sqlite3 **db) {
    int rc = sqlite3_open("mes_factory.db", db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "DB 연결 에러: %s\n", sqlite3_errmsg(*db));
        exit(1);
    }

    char *err_msg = 0;
    // 5M 데이터 정규화 반영 스키마 구조
    char *sql = "CREATE TABLE IF NOT EXISTS employee ("
                "  emp_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "  name TEXT NOT NULL, "
                "  department TEXT NOT NULL);"
                "CREATE TABLE IF NOT EXISTS qualification ("
                "  emp_id INTEGER PRIMARY KEY, "
                "  qual_name TEXT NOT NULL,"
                "  FOREIGN KEY(emp_id) REFERENCES employee(emp_id));"
                "CREATE TABLE IF NOT EXISTS attendance ("
                "  emp_id INTEGER PRIMARY KEY, "
                "  is_present INTEGER DEFAULT 0,"
                "  FOREIGN KEY(emp_id) REFERENCES employee(emp_id));";

    rc = sqlite3_exec(*db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "테이블 스키마 생성 오류: %s\n", err_msg);
        sqlite3_free(err_msg);
    }
}

// 실행 첫 화면에 전체 메뉴를 표출하는 통합 대시보드 함수 (Switch-case 제어)
void run_integrated_mes_menu(sqlite3 *db) {
    int choice;
    while (1) {
        printf("\n================================\n");
        printf("ERP / MES 통합 생산 프로그램 (Main)\n");
        printf("================================\n");
        printf("[1. 인사관리 - 1-1) 근태관리 기능]\n");
        printf("  1. 신규 직원 등록 (자격 매칭 포함)\n");
        printf("  2. 출근 체크\n");
        printf("  3. 출근 현황 조회 (조건: Present)\n");
        printf("  4. 결근 직원 조회 (조건: Absent)\n");
        printf("  5. 전체 직원 조회\n");
        printf("--------------------------------\n");
        printf("[기타 확장 모듈 - 향후 개발 연계 예정]\n");
        printf("  6. 자재추적관리 (Material)\n");
        printf("  7. 생산공정관리 (Machine/Method)\n");
        printf("  8. 품질보증관리 / 4-1) 자격관리 (Measure)\n");
        printf("  9. 설계관리 / 고객관리 / 출하관리\n");
        printf("  0. 프로그램 완전히 종료\n");
        printf("================================\n");
        printf("메뉴 선택 : ");
        
        if (scanf("%d", &choice) != 1) {
            while (getchar() != '\n'); 
            continue;
        }

        switch (choice) {
            case 1: register_employee(db); break;
            case 2: check_in_employee(db); break;
            case 3: view_present_employees(db); break;
            case 4: view_absent_employees(db); break;
            case 5: view_all_employees(db); break;
            case 0: return; 
            case 6: case 7: case 8: case 9:
                printf("\n[안내] 해당 모듈은 인사/근태 마스터 데이터 구축 완료 후 연동되는 모듈입니다.\n");
                break;
            default: 
                printf("\n[오류] 없는 메뉴 번호입니다. 다시 입력해 주세요.\n"); 
                break;
        }
    }
}

// 1. 신규 직원 등록 및 4-1) 자격 유형 선택
void register_employee(sqlite3 *db) {
    Employee emp;
    sqlite3_stmt *res;
    int qual_choice;
    
    printf("\n[직원 등록]\n");
    printf("직원 이름 입력 : ");
    scanf("%s", emp.name);
    printf("부서 입력 : ");
    scanf("%s", emp.department);

    // 고압용기 제조 분야의 필수 직무 자격 분류 (4-1 자격관리 연계)
    printf("\n[4-1 자격관리] 직무 필수 자격증 유형을 지정하세요:\n");
    printf("1. 내부감사자  2. 검사자  3. 용접사\n");
    printf("4. 설계사      5. 시험자  6. 비파괴 검사자\n");
    printf("자격 번호 입력 : ");
    scanf("%d", &qual_choice);

    switch(qual_choice) {
        case 1: strcpy(emp.qualification, "내부감사자"); break;
        case 2: strcpy(emp.qualification, "검사자"); break;
        case 3: strcpy(emp.qualification, "용접사"); break;
        case 4: strcpy(emp.qualification, "설계사"); break;
        case 5: strcpy(emp.qualification, "시험자"); break;
        case 6: strcpy(emp.qualification, "비파괴 검사자"); break;
        default: strcpy(emp.qualification, "일반작업자"); break;
    }

    // employee 마스터 테이블 저장
    char *sql1 = "INSERT INTO employee (name, department) VALUES (?, ?);";
    sqlite3_prepare_v2(db, sql1, -1, &res, 0);
    sqlite3_bind_text(res, 1, emp.name, -1, SQLITE_STATIC);
    sqlite3_bind_text(res, 2, emp.department, -1, SQLITE_STATIC);
    sqlite3_step(res);
    sqlite3_finalize(res);

    int last_id = (int)sqlite3_last_insert_rowid(db);

    // qualification 정규화 테이블 저장
    char *sql2 = "INSERT INTO qualification (emp_id, qual_name) VALUES (?, ?);";
    sqlite3_prepare_v2(db, sql2, -1, &res, 0);
    sqlite3_bind_int(res, 1, last_id);
    sqlite3_bind_text(res, 2, emp.qualification, -1, SQLITE_STATIC);
    sqlite3_step(res);
    sqlite3_finalize(res);

    // attendance 정규화 테이블 초기값 저장 (0:결근상태)
    char *sql3 = "INSERT INTO attendance (emp_id, is_present) VALUES (?, 0);";
    sqlite3_prepare_v2(db, sql3, -1, &res, 0);
    sqlite3_bind_int(res, 1, last_id);
    sqlite3_step(res);
    sqlite3_finalize(res);

    printf("\n직원 등록이 완료되었습니다.\n");
    printf("\n저장되는 데이터 예\n");
    printf("emp_id : %d\n", last_id);
    printf("name : %s\n", emp.name);
    printf("department : %s\n", emp.department);
    printf("is_present : 0\n");
}

// 2. 출근 체크 처리 함수
void check_in_employee(sqlite3 *db) {
    int target_id;
    sqlite3_stmt *res;

    printf("\n[출근 처리]\n");
    printf("직원 번호 입력 : ");
    scanf("%d", &target_id);

    char *sql_select = "SELECT name, department FROM employee WHERE emp_id = ?;";
    sqlite3_prepare_v2(db, sql_select, -1, &res, 0);
    sqlite3_bind_int(res, 1, target_id);

    if (sqlite3_step(res) == SQLITE_ROW) {
        char name[20];
        char dept[30];
        strcpy(name, (const char*)sqlite3_column_text(res, 0));
        strcpy(dept, (const char*)sqlite3_column_text(res, 1));
        sqlite3_finalize(res);

        // 출근 데이터 유무 플래그 업데이트
        char *sql_update = "UPDATE attendance SET is_present = 1 WHERE emp_id = ?;";
        sqlite3_prepare_v2(db, sql_update, -1, &res, 0);
        sqlite3_bind_int(res, 1, target_id);
        sqlite3_step(res);
        sqlite3_finalize(res);

        printf("\n%s 직원의 출근 처리가 완료되었습니다.\n", name);
        printf("\n출근 처리 후 데이터\n");
        printf("emp_id : %d\n", target_id);
        printf("name : %s\n", name);
        printf("department : %s\n", dept);
        printf("is_present : 1\n");
    } else {
        printf("\n[안내] 해당 사번 번호의 직원을 찾을 수 없습니다.\n");
        sqlite3_finalize(res);
    }
}

// 3. 출근 직원 조회 (WHERE is_present = 1)
void view_present_employees(sqlite3 *db) {
    sqlite3_stmt *res;
    char *sql = "SELECT e.emp_id, e.name, e.department, q.qual_name FROM employee e "
                "JOIN attendance a ON e.emp_id = a.emp_id "
                "JOIN qualification q ON e.emp_id = q.emp_id WHERE a.is_present = 1;";

    printf("\n[출근 직원 조회]\n\n");
    printf("%-6s %-10s %-15s %-15s\n", "번호", "이름", "부서", "보유 자격");
    printf("------------------------------------------------------------\n");

    sqlite3_prepare_v2(db, sql, -1, &res, 0);
    while (sqlite3_step(res) == SQLITE_ROW) {
        printf("%-6d %-10s %-15s %-15s\n", 
               sqlite3_column_int(res, 0),
               sqlite3_column_text(res, 1),
               sqlite3_column_text(res, 2),
               sqlite3_column_text(res, 3));
    }
    sqlite3_finalize(res);
}

// 4. 결근 직원 조회 (WHERE is_present = 0)
void view_absent_employees(sqlite3 *db) {
    sqlite3_stmt *res;
    char *sql = "SELECT e.emp_id, e.name, e.department, q.qual_name FROM employee e "
                "JOIN attendance a ON e.emp_id = a.emp_id "
                "JOIN qualification q ON e.emp_id = q.emp_id WHERE a.is_present = 0;";

    printf("\n[결근 직원 조회]\n\n");
    printf("%-6s %-10s %-15s %-15s\n", "번호", "이름", "부서", "보유 자격");
    printf("------------------------------------------------------------\n");

    sqlite3_prepare_v2(db, sql, -1, &res, 0);
    while (sqlite3_step(res) == SQLITE_ROW) {
        printf("%-6d %-10s %-15s %-15s\n", 
               sqlite3_column_int(res, 0),
               sqlite3_column_text(res, 1),
               sqlite3_column_text(res, 2),
               sqlite3_column_text(res, 3));
    }
    sqlite3_finalize(res);
}

// 5. 전체 직원 조회
void view_all_employees(sqlite3 *db) {
    sqlite3_stmt *res;
    char *sql = "SELECT e.emp_id, e.name, e.department, a.is_present, q.qual_name FROM employee e "
                "JOIN attendance a ON e.emp_id = a.emp_id "
                "JOIN qualification q ON e.emp_id = q.emp_id;";

    printf("\n[전체 직원 조회]\n\n");
    printf("%-6s %-10s %-15s %-10s %-15s\n", "번호", "이름", "부서", "출근상태", "보유 자격");
    printf("----------------------------------------------------------------------\n");

    sqlite3_prepare_v2(db, sql, -1, &res, 0);
    while (sqlite3_step(res) == SQLITE_ROW) {
        int is_present = sqlite3_column_int(res, 3);
        printf("%-6d %-10s %-15s %-10s %-15s\n", 
               sqlite3_column_int(res, 0),
               sqlite3_column_text(res, 1),
               sqlite3_column_text(res, 2),
               is_present ? "출근" : "결근",
               sqlite3_column_text(res, 4));
    }
    sqlite3_finalize(res);
}