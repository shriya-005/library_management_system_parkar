from services.book_service import (
    add_book,
    display_book,
    search_books,
    remove_book
)

from services.member_service import (
    register_member,
    display_members
)

from services.borrow_service import (
    borrow_book,
    return_book
)

from storage.storage import load_data, save_data


def show_menu():
    print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
    print("1. Add Book")
    print("2. Display All Books")
    print("3. Search Books")
    print("4. Register Member")
    print("5. Display All Members")
    print("6. Borrow Book")
    print("7. Return Book")
    print("8. Remove Book")
    print("9. Save and Exit")
    print("================================================")


def show_result(result):
    if result["success"]:
        print("SUCCESS:", result["message"])
    else:
        print("ERROR:", result["message"])


def main():
    # Load saved records when the application starts
    data = load_data()

    books = data["books"]
    members = data["members"]

    print("Welcome to the Library Management System!")

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            book_id = input("Enter Book ID: ").strip()
            title = input("Enter Book Title: ").strip()
            author = input("Enter Author Name: ").strip()

            result = add_book(books, book_id, title, author)
            show_result(result)

            if result["success"]:
                save_data(books, members)

        elif choice == "2":
            books_list = display_book(books)
            if not books_list:
                print("No books available.")
            else:
                print("\nAvailable Books:")
                for book in books_list:
                    status = (
                        "Available"
                        if book["borrowed_by"] is None
                        else "On Loan"
                    )
                    print(
                        f'{book["book_id"]} | '
                        f'{book["title"]} | '
                        f'{book["author"]} | {status}'
                    )

        elif choice == "3":
            query = input("Enter title or author to search: ").strip()

            results = search_books(books, query)
            show_result(results)

            if results["success"] and results["data"]:
                for book in results["data"]:
                    status = (
                        "Available"
                        if book["borrowed_by"] is None
                        else "On Loan"
                    )

                    print(
                        f'{book["book_id"]} | '
                        f'{book["title"]} | '
                        f'{book["author"]} | {status}'
                    )

        elif choice == "4":
            member_id = input("Enter Member ID: ").strip()
            name = input("Enter Member Name: ").strip()

            result = register_member(members, member_id, name)
            show_result(result)

            if result["success"]:
                save_data(books, members)

        elif choice == "5":
            result = display_members(members)
            show_result(result)
            if result["success"] and result["data"]:
                for member in result["data"]:
                    borrowed = ", ".join(member["borrowed_books"]) if member["borrowed_books"] else "None"
                    print(f"ID: {member['member_id']} | Name: {member['name']} | Borrowed Books: {borrowed}")

        elif choice == "6":
            member_id = input("Enter Member ID: ").strip()
            book_id = input("Enter Book ID: ").strip()

            result = borrow_book(
                books, members, member_id, book_id
            )
            show_result(result)

            if result["success"]:
                save_data(books, members)

        elif choice == "7":
            member_id = input("Enter Member ID: ").strip()
            book_id = input("Enter Book ID: ").strip()

            result = return_book(
                books, members, member_id, book_id
            )
            show_result(result)

            if result["success"]:
                save_data(books, members)

        elif choice == "8":
            book_id = input("Enter Book ID to remove: ").strip()

            result = remove_book(books, book_id)
            show_result(result)

            if result["success"]:
                save_data(books, members)

        elif choice == "9":
            save_data(books, members)
            print("Records saved successfully.")
            print("Exiting Library Management System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()

