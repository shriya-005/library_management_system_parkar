import json 
from pathlib import Path
import streamlit as st
from services.borrow_service import (
    borrow_book as borrow_book_service,
    return_book as return_book_service,
)

DATA_DIR= Path("data")
DATA_FILE= DATA_DIR / "library.json"
MAX_BOOKS_PER_MEMBER= 3

st.set_page_config(page_title="Library Management System", layout="wide",)

def load_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        return {"books": [], "members": []}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        data.setdefault("books", [])
        data.setdefault("members", [])
        return data

    except (json.JSONDecodeError, OSError):
        st.error("Unable to read library data. Please check data/library.json file.")
        st.stop()

def save_data(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    temp_file = DATA_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    temp_file.replace(DATA_FILE)

data=load_data()
books=data["books"]
members=data["members"]

available_books = [book for book in books if book.get("borrowed_by") is None]

borrowed_books = [book for book in books if book.get("borrowed_by") is not None]

st.title("Library Management System")
st.caption("Book, Member, and Borrowing & Returning Management")

total_col, available_col, borrowed_col, members_col = st.columns(4)
total_col.metric("Total Books", len(books))
available_col.metric("Available Books", len(available_books))
borrowed_col.metric("Borrowed Books", len(borrowed_books))
members_col.metric("Total Members", len(members))

st.divider()

page=st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Book", "Add Member", "Borrow Book", "Return Book"],
)

if page == "Dashboard":
    st.header("Dashboard")
    st.write("Welcome to the Library Management System!")

    if books:
        st.subheader("Available Books")

        st.dataframe(
            [
                {
                    "Book ID": b["book_id"],
                    "Title": b["title"],
                    "Author": b["author"],
                    "Status":( "Available" if b.get("borrowed_by") is None else "Borrowed"
                    ),
                }
                for b in books
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No books have been added yet. Please add books to the library.")

elif page == "Add Book":
    st.header("Books Management")

    with st.expander("Add New Book"):
        with st.form("add_book_form"):
            book_id = st.text_input("Book ID").strip()
            title = st.text_input("Title").strip()
            author = st.text_input("Author").strip()
            submitted= st.form_submit_button("Add Book")

            if submitted:
                if not book_id or not title or not author:
                    st.error("pls fill all fields.")
                elif any(b["book_id"].casefold() == book_id.casefold() for b in books):
                    st.error("This book ID already exists. Please use a unique ID.")
                else:
                    books.append({
                        "book_id": book_id,
                        "title": title,
                        "author": author,
                        "borrowed_by": None,
                    })
                    save_data({"books": books, "members": members})
                    st.success("Book added successfully!")
                    st.rerun()

        st.subheader("Search Books")
        query = st.text_input("Search by Title or Author").strip().casefold()

        filtered_books = [
            b for b in books
            if query in b["title"].casefold() or query in b["author"].casefold()
        ] 

        if filtered_books:
            st.dataframe(
                [
                    {
                        "Book ID": b["book_id"],
                        "Title": b["title"],
                        "Author": b["author"],
                        "Status": ("Available" if b.get("borrowed_by") is None else "Borrowed"),
                    }
                    for b in filtered_books
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No books found matching the search criteria.")

        st.subheader("Remove Book")
        removable_books = [b for b in books if b.get("borrowed_by") is None]
        if removable_books:
            selected_book=st.selectbox(
                "Select available book to remove", 
                removable_books,
                format_func=lambda b: f"{b['book_id']} - {b['title']} ",
            )

            if st.button("Remove Selected Book"):
                books.remove(selected_book)
                save_data({"books": books, "members": members})
                st.success("Book removed successfully!")
                st.rerun()

        else:
            st.info("No available books to remove.")

elif page == "Add Member":
    st.header("Members Management")

    with st.form("register_member_form"):
        member_id = st.text_input("Member ID").strip()
        name = st.text_input("Name").strip()
        submitted= st.form_submit_button("Register Member")

        if submitted:
            if not member_id or not name:
                st.error("Member ID and Name are required.")
            elif any(m["member_id"].casefold() == member_id.casefold() for m in members):
                st.error("This member ID already exists. Please use a unique ID.")
            else:
                members.append({
                    "member_id": member_id,
                    "name": name,
                    "borrowed_books": [],
                })
                save_data({"books": books, "members": members})
                st.success("Member registered successfully!")
                st.rerun()

    st.subheader("Registered Members")
    if members:
        st.dataframe(
            [
                {
                    "Member ID": m["member_id"],
                    "Name": m["name"],
                    "Borrowed Books": len(m.get("borrowed_books", [])),
                }
                for m in members
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No members have been registered yet. Please register members.")

elif page == "Borrow Book":
    st.header("Borrowing Management")

    if not members:
        st.warning("Register member first before borrowing books.")

    elif not available_books:
        st.warning("No available books to borrow. Please add books to the library.")

    else:
        member = st.selectbox(
            "Select Member",
            members,
            format_func=lambda m: f"{m['member_id']} - {m['name']}",
            key="borrow_member",
        )

        member_loans = member.setdefault("borrowed_books", [])
        st.write(
            f"Borrowed Books: {len(member_loans)} "
            f"out of {MAX_BOOKS_PER_MEMBER}"
        )

        with st.form("borrow_book_form"):
            book = st.selectbox(
                "Select Book to Borrow",
                available_books,
                format_func=lambda b: f"{b['book_id']} - {b['title']}",
                key="borrow_book",
            )
            submitted = st.form_submit_button(
                "Borrow Book",
                key="borrow_book_submit",
                type="primary",
            )

        if submitted:
            result = borrow_book_service(
                books, members, member["member_id"], book["book_id"]
            )
            if result["success"]:
                save_data({"books": books, "members": members})
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

elif page == "Return Book":
    st.header("Returning Management")

    member_with_loans = [m for m in members if m.get("borrowed_books")]

    if not member_with_loans:
        st.info("No members have borrowed books yet.")
    else:
        member = st.selectbox(
            "Select Member",
            member_with_loans,
            format_func=lambda m: f"{m['member_id']} - {m['name']}",
            key="return_member",
        )

        loaned_ids = member.get("borrowed_books", [])
        member_books = [
            b for b in books
            if b["book_id"] in loaned_ids
            and b.get("borrowed_by") == member["member_id"]
        ]

        if member_books:
            with st.form("return_book_form"):
                book = st.selectbox(
                    "Select Book to Return",
                    member_books,
                    format_func=lambda b: f"{b['book_id']} - {b['title']}",
                    key="return_book",
                )
                submitted = st.form_submit_button(
                    "Return Book",
                    key="return_book_submit",
                    type="primary",
                )

            if submitted:
                result = return_book_service(
                    books, members, member["member_id"], book["book_id"]
                )
                if result["success"]:
                    save_data({"books": books, "members": members})
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])
        else:
            st.info("No matching books found for this member.")

st.sidebar.divider()
