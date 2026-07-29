import os
import sqlite3

# 0. 경로 설정 및 파일 분리

DB_DIR = "/home/smart/work/dbfiles"

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

FRIENDS_DB_PATH = os.path.join(DB_DIR, "friends.db")
HOBBY_DB_PATH = os.path.join(DB_DIR, "hobby.db")


# 전화번호 포맷팅 함수
def format_phone_number(raw_number):
    digits = "".join(filter(str.isdigit, raw_number))
    length = len(digits)

    if digits.startswith("02"):
        if length == 9: return f"{digits[:2]}-{digits[2:5]}-{digits[5:]}"
        elif length == 10: return f"{digits[:2]}-{digits[2:6]}-{digits[6:]}"
    elif digits.startswith("0"):
        if length == 10: return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif length == 11: return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"
    elif length == 8: return f"{digits[:4]}-{digits[4:]}"

    return raw_number

# 1. Database & Repository Layer (데이터 계층)

class FriendRepository:
    def __init__(self):
        self.friends_db = FRIENDS_DB_PATH
        self.hobby_db = HOBBY_DB_PATH
        self.init_db()

    def _connect(self):
        conn = sqlite3.connect(self.friends_db)
        conn.row_factory = sqlite3.Row
        conn.execute(f"ATTACH DATABASE '{self.hobby_db}' AS hobby_db")
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self):
        with sqlite3.connect(self.friends_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS friends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    address TEXT,
                    phone TEXT,
                    memo TEXT
                )
            """)
            
        with sqlite3.connect(self.hobby_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS hobbies (
                    hobby_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    friend_id INTEGER NOT NULL,
                    hobby TEXT,
                    favorite_food TEXT
                )
            """)

    def get_simple_list(self):
        with self._connect() as conn:
            cursor = conn.execute("SELECT id, name FROM friends ORDER BY id")
            return [dict(row) for row in cursor.fetchall()]

    def get_all_friends_detail(self, order_by_name=False):
        sort_column = "f.name ASC" if order_by_name else "f.id ASC"
        
        query = f"""
            SELECT 
                f.id, f.name, f.address, f.phone, f.memo,
                COALESCE(h.hobby, '-') AS hobby,
                COALESCE(h.favorite_food, '-') AS favorite_food
            FROM friends f
            LEFT JOIN hobby_db.hobbies h ON f.id = h.friend_id
            ORDER BY {sort_column}
        """
        with self._connect() as conn:
            cursor = conn.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def add_friend(self, name, address, phone, memo, hobby, favorite_food):
        conn = self._connect()
        try:
            with conn:
                cursor = conn.execute("""
                    INSERT INTO friends (name, address, phone, memo) 
                    VALUES (?, ?, ?, ?)
                """, (name, address, phone, memo))
                
                friend_id = cursor.lastrowid
                
                conn.execute("""
                    INSERT INTO hobby_db.hobbies (friend_id, hobby, favorite_food)
                    VALUES (?, ?, ?)
                """, (friend_id, hobby, favorite_food))
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def delete_friend(self, name):
        conn = self._connect()
        try:
            with conn:
                cursor = conn.execute("SELECT id FROM friends WHERE name = ?", (name,))
                row = cursor.fetchone()
                if not row:
                    return 0
                
                friend_id = row["id"]
                
                conn.execute("DELETE FROM hobby_db.hobbies WHERE friend_id = ?", (friend_id,))
                cursor = conn.execute("DELETE FROM friends WHERE id = ?", (friend_id,))
                return cursor.rowcount
        except sqlite3.Error:
            return 0
        finally:
            conn.close()

    def update_name(self, old_name, new_name):
        with self._connect() as conn:
            try:
                cursor = conn.execute(
                    "UPDATE friends SET name = ? WHERE name = ?",
                    (new_name, old_name)
                )
                return cursor.rowcount
            except sqlite3.IntegrityError:
                return -1

# 2. Service & UI Controller Layer (비즈니스/입출력 계층)

class FriendManagerApp:
    def __init__(self):
        self.repo = FriendRepository()

    def display_menu(self):
        print("\n1. 친구 리스트 출력 (이름만)")
        print("2. 친구 추가 (전체 정보 + 취미/음식)")
        print("3. 친구 삭제")
        print("4. 이름 변경")
        print("5. 친구 상세 정보 전체 출력 (등록순)")
        print("6. 친구 상세 정보 전체 출력 (이름순 정렬)")
        print("9. 종료")

    def run(self):
        while True:
            self.display_menu()
            try:
                choice = int(input("메뉴를 선택하시오: "))
            except ValueError:
                print("[오류] 숫자로 메뉴를 선택해주세요.")
                continue

            if choice == 1:
                friends = self.repo.get_simple_list()
                print("\n=== 친구 리스트 ===")
                if not friends:
                    print("등록된 친구가 없습니다.")
                for f in friends:
                    # [수정] '이름: ' 문구를 제거하고 값만 출력
                    print(f"[{f['id']}] {f['name']}")

            elif choice == 2:
                name = input("이름을 입력하시오: ").strip()
                if not name:
                    print("[오류] 이름은 필수 입력 항목입니다.")
                    continue
                
                address = input("주소를 입력하시오: ").strip()
                raw_phone = input("전화번호를 입력하시오 (숫자만 입력 가능): ").strip()
                formatted_phone = format_phone_number(raw_phone)
                memo = input("메모를 입력하시오: ").strip()
                
                hobby = input("취미를 입력하시오: ").strip()
                favorite_food = input("좋아하는 음식을 입력하시오: ").strip()
                
                success = self.repo.add_friend(name, address, formatted_phone, memo, hobby, favorite_food)
                if success:
                    print(f"[안내] {name} 님의 정보가 분리된 DB 파일에 각각 안전하게 저장되었습니다.")
                else:
                    print(f"[오류] 이미 존재하는 이름입니다. '{name}' 이름은 중복 등록할 수 없습니다.")

            elif choice == 3:
                name = input("삭제할 친구의 이름을 입력하시오: ")
                deleted = self.repo.delete_friend(name)
                if deleted > 0:
                    print(f"[안내] {name} 친구를 삭제했습니다.")
                else:
                    print("[오류] 일치하는 이름이 없습니다.")

            elif choice == 4:
                old_name = input("기존 이름을 입력하시오: ")
                new_name = input("변경할 새 이름을 입력하시오: ")
                if new_name.strip():
                    updated = self.repo.update_name(old_name, new_name)
                    if updated > 0:
                        print(f"[안내] {old_name}에서 {new_name}(으)로 이름이 변경되었습니다.")
                    elif updated == -1:
                        print(f"[오류] 변경하려는 이름 '{new_name}'이(가) 이미 존재하여 변경할 수 없습니다.")
                    else:
                        print("[오류] 기존 이름과 일치하는 친구가 없습니다.")
                else:
                    print("[오류] 새 이름은 비어둘 수 없습니다.")

            elif choice == 5 or choice == 6:
                is_name_sort = True if choice == 6 else False
                friends = self.repo.get_all_friends_detail(order_by_name=is_name_sort)
                
                title = "이름순 정렬" if is_name_sort else "등록순"
                print(f"\n=== 친구 상세 목록 ({title}) ===")
                
                if not friends:
                    print("등록된 친구가 없습니다.")
                else:
                    print("-" * 110)
                    print(f"{'ID':<4} | {'이름':<10} | {'주소':<15} | {'연락처':<13} | {'취미':<10} | {'좋아하는 음식':<12} | {'메모'}")
                    print("-" * 110)
                    for f in friends:
                        # [수정] 각 데이터 행에서 '주소: ', '연락처: ' 등의 텍스트를 제거하고 입력값만 맵핑
                        print(f"[{f['id']}] {f['name']:<10} | {f['address']:<15} | {f['phone']:<13} | {f['hobby']:<10} | {f['favorite_food']:<12} | {f['memo']}")
                    print("-" * 110)

            elif choice == 9:
                print("프로그램을 종료합니다.")
                break
            else:
                print("[오류] 잘못된 메뉴 번호입니다. 다시 선택해주세요.")

# 3. Main Entry (프로그램 진입점)

def main():
    app = FriendManagerApp()
    app.run()


if __name__ == "__main__":
    main()
