#include <stdio.h>
#include <sqlite3.h>
#include <stdlib.h>

int main()
{
    sqlite3 *db;
    char *errMsg = NULL;
    sqlite3_open("home/smart/work/dbfiles/person.db", &db);

 if (sqlite3_open("person.db", &db) != SQLITE_OK)
    {
        printf("데이터베이스 열기 실패\n");
        return 1;
    }

    //01.person 테이블 생성
    const char *sql =
        "CREATE TABLE IF NOT EXISTS person ("
        "id INTEGER PRIMARY KEY,"
        "name TEXT NOT NULL,"
        "phone TEXT"
        ");";

    if (sqlite3_exec(db, sql, NULL, NULL, &errMsg) != SQLITE_OK)
    {
        printf("테이블 생성 실패 : %s\n", errMsg);
        sqlite3_free(errMsg);
    }
    else
    {
        printf("person 테이블 생성 완료\n");
    }

    //리소스 종료
    sqlite3_close(db);
    return 0;
}