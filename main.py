from queries import *
from db import cursor, conn, print_all_tables, insert_data, create_tables


def main():
    while True:
        print("Оберіть запит:")
        print("1. Інформація про покупки")
        print("2. Одяг за вибраним типом")
        print("3. Кількість покупок для кожного клієнта:")
        print("4. Вартість кожної покупки без знижки та з урахуванням:")
        print("5. Загальна сума витрат кожного клієнта:")
        print("6. Кількість кожного виду одягу на кожному складі (перехресний запит):")
        print("0. Вийти.")

        choice = input("Ваш вибір: ")
        if choice == "1":
            query_1()
        elif choice == "2":
            source = input("Введіть клієнта: ")
            query_2(source)
        elif choice == "3":
            query_3()
        elif choice == "4":
            query_4()
        elif choice == "5":
            query_5()
        elif choice == "6":
            query_6()
        elif choice == "0":
            break
        else:
            print("Невірний вибір!")


if __name__ == "__main__":
    create_tables()
    insert_data()
    print_all_tables()
    main()
    cursor.close()
    conn.close()
