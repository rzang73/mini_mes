#include <iostream>
#include <vector>
#include <string>
#include <iomanip>

// ==========================================
// 1. Product 클래스 (부품 개별 객체)
// ==========================================
class Product {
private:
    int id;
    std::string name;
    int quantity;
    int price;

public:
    // 생성자
    Product(int id, std::string name, int quantity, int price)
        : id(id), name(name), quantity(quantity), price(price) {}

    // Getter 함수 (정보 은닉 보호)
    int getId() const { return id; }
    int getQuantity() const { return quantity; }

    // 비즈니스 로직에 따른 내부 상태 변경 메서드
    void addQuantity(int amount) { quantity += amount; }
    void removeQuantity(int amount) { quantity -= amount; }

    // 스스로의 정보를 출력하는 메서드
    void print() const {
        std::cout << id << "\t" 
                  << std::left << std::setw(15) << name << "\t" 
                  << quantity << "개\t" 
                  << price << "원" << std::endl;
    }
};

// ==========================================
// 2. PartsManager 클래스 (재고 관리 시스템 제어 및 로직 담당)
// ==========================================
class PartsManager {
private:
    std::vector<Product> products; // 부품 목록을 캡슐화하여 내부에서 관리

    // 내부에서만 사용하는 헬퍼 메서드 (ID로 인덱스 검색)
    int findProductIndex(int id) const {
        for (size_t i = 0; i < products.size(); ++i) {
            if (products[i].getId() == id) {
                return i;
            }
        }
        return -1;
    }

public:
    // 생성자: 초기 기본 데이터 세팅
    PartsManager() {
        products.emplace_back(1001, "타이어", 20, 120000);
        products.emplace_back(1002, "와이퍼", 35, 15000);
        products.emplace_back(1003, "엔진오일", 50, 35000);
        products.emplace_back(1004, "배터리", 12, 90000);
        products.emplace_back(1005, "브레이크패드", 25, 60000);
        products.emplace_back(1006, "에어컨필터", 40, 18000);
        products.emplace_back(1007, "전조등", 18, 45000);
    }

    // 메뉴 출력
    void printMenu() const {
        std::cout << "\n==== 자동차 부품 재고 관리 프로그램 (OOP) ====\n";
        std::cout << "1. 전체 재고 조회\n";
        std::cout << "2. 부품 검색\n";
        std::cout << "3. 입고 처리\n";
        std::cout << "4. 출고 처리\n";
        std::cout << "5. 신규 부품 등록\n";
        std::cout << "0. 종료\n";
        std::cout << "메뉴 선택: ";
    }

    // 1. 전체 재고 조회
    void printAllProducts() const {
        std::cout << "\nID\t부품명\t\t수량\t가격\n";
        std::cout << "----------------------------------------\n";
        for (const auto& product : products) {
            product.print();
        }
    }

    // 2. 부품 검색
    void searchProduct() const {
        int id;
        std::cout << "검색할 부품 ID 입력: ";
        std::cin >> id;

        int index = findProductIndex(id);
        if (index == -1) {
            std::cout << "해당 부품을 찾을 수 없습니다.\n";
        } else {
            std::cout << "\nID\t부품명\t\t수량\t가격\n";
            std::cout << "----------------------------------------\n";
            products[index].print();
        }
    }

    // 3. 입고 처리
    void stockIn() {
        int id, amount;
        std::cout << "입고할 부품 ID 입력: ";
        std::cin >> id;

        int index = findProductIndex(id);
        if (index == -1) {
            std::cout << "해당 부품을 찾을 수 없습니다.\n";
            return;
        }

        std::cout << "입고 수량 입력: ";
        std::cin >> amount;

        if (amount <= 0) {
            std::cout << "입고 수량은 1개 이상이어야 합니다.\n";
            return;
        }

        products[index].addQuantity(amount);
        std::cout << "입고 처리가 완료되었습니다.\n";
        std::cout << "현재 재고: " << products[index].getQuantity() << "개\n";
    }

    // 4. 출고 처리
    void stockOut() {
        int id, amount;
        std::cout << "출고할 부품 ID 입력: ";
        std::cin >> id;

        int index = findProductIndex(id);
        if (index == -1) {
            std::cout << "해당 부품을 찾을 수 없습니다.\n";
            return;
        }

        std::cout << "출고 수량 입력: ";
        std::cin >> amount;

        if (amount <= 0) {
            std::cout << "출고 수량은 1개 이상이어야 합니다.\n";
            return;
        }

        if (products[index].getQuantity() < amount) {
            std::cout << "재고가 부족합니다.\n";
            std::cout << "현재 재고: " << products[index].getQuantity() << "개\n";
            return;
        }

        products[index].removeQuantity(amount);
        std::cout << "출고 처리가 완료되었습니다.\n";
        std::cout << "현재 재고: " << products[index].getQuantity() << "개\n";
    }

    // 5. 신규 부품 등록
    void addProduct() {
        int id, quantity, price;
        std::string name;

        std::cout << "신규 부품 ID 입력: ";
        std::cin >> id;

        if (findProductIndex(id) != -1) {
            std::cout << "이미 존재하는 ID입니다.\n";
            return;
        }

        std::cout << "부품명 입력: ";
        std::cin >> name;

        std::cout << "재고 수량 입력: ";
        std::cin >> quantity;

        std::cout << "가격 입력: ";
        std::cin >> price;

        products.emplace_back(id, name, quantity, price);
        std::cout << "신규 부품이 등록되었습니다.\n";
    }

    // 시스템 실행 메인 루프 컨트롤러
    void run() {
        int choice;
        while (true) {
            printMenu();
            std::cin >> choice;

            if (choice == 1) printAllProducts();
            else if (choice == 2) searchProduct();
            else if (choice == 3) stockIn();
            else if (choice == 4) stockOut();
            else if (choice == 5) addProduct();
            else if (choice == 0) {
                std::cout << "프로그램을 종료합니다.\n";
                break;
            } else {
                std::cout << "잘못된 메뉴입니다.\n";
            }
        }
    }
};

// ==========================================
// 3. 메인 함수 (진입점)
// ==========================================
int main() {
    // 관리자 객체 생성 후 실행
    PartsManager manager;
    manager.run();

    return 0;
}