#include <stdio.h>
#include <sqlite3.h>

int main()
{
    sqlite3 *db;
    char *errMsg = NULL;

    //
    if(sqlite3_open("/home/smart/work/dbfiles/person.db", &db) != SQLITE_OK){
        printf("테이블생성 실패\n"); 
        exit(1); db 파일 열지 못하고 종료
    };

    // 데이터 삽입
    const char *sql =
        "INSERT INTO person VALUES"
        "(1,'Hong Gil Dong','010-1234-5678'),"
        "(2,'Lee Sun Shin','010-2345-6789'),"
        "(3,'Kim Yu Shin','010-3456-7890'),"
        "(4,'Park Ji Sung','010-4567-8901'),"
        "(5,'Choi Min Soo','010-5678-9012');";

    If(sqlite3_exec(db, sql, NULL, NULL, &errMsg) != SQLITE_OK)
    {
        printf("person 데이터 삽입 실패\n");
    }
    else
    {
        printf("person 데이터 삽입 완료 \n");
    }
    sqlite_close(db);
    return 0;
}