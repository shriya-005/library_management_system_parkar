def borrow_book(books, members, member_id,book_id ):
    member = next( (m for m in members if m["member_id"] == member_id), None)

    if member is None:
        return {
            "success": False,
            "message": "Member not found.",
            "data": None
        }

    book = next((b for b in books if b["book_id"] == book_id), None)

    if book is None:
        return {
            "success": False,
            "message": "Book not found.",
            "data": None
        }

    if book["borrowed_by"] is not None:
        return {
            "success": False,
            "message": "Book is already borrowed.",
            "data": None
        }

    if len(member["borrowed_books"]) >= 3:
        return {
            "success": False,
            "message": "Member has already borrowed the maximum number of books.",
            "data": None
        }

    book["borrowed_by"] = member_id
    member["borrowed_books"].append(book_id)

    return {
        "success": True,
        "message": "Book borrowed successfully.",
        "data": book
    }

def return_book(books, members, member_id, book_id):
    member = next((m for m in members if m["member_id"] == member_id), None)

    if member is None:
        return {
            "success": False,
            "message": "Member not found.",
            "data": None
        }

    book = next((b for b in books if b["book_id"] == book_id), None)

    if book is None:
        return {
            "success": False,
            "message": "Book not found.",
            "data": None
        }

    if book["borrowed_by"] != member_id:
        return {
            "success": False,
            "message": "This book was not borrowed by this member.",
            "data": None
        }

    book["borrowed_by"] = None
    member["borrowed_books"].remove(book_id)
    return {
        "success": True,
        "message": "Book returned successfully.",
        "data": book
    }