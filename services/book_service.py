def add_book(books, book_id, title, author):
    book_id=book_id.strip()
    title=title.strip()
    author=author.strip()

    if not book_id or not title or not author:
        return {
            "success": False,
            "message": "Book ID, title, and author are required.",
            "data": None
        }

    for book in books:
        if book['book_id'] == book_id:
            return {
                "success": False,
                "message": "A book with this ID already exists.",
                "data": None
            }

    new_book = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "borrowed_by": None
    }

    books.append(new_book)
    return {
        "success": True,
        "message": "Book added successfully.",
        "data": new_book
    }

def display_book(book):
    result = []
    for book in book:
        book_info = book.copy()

        if book_info['borrowed_by'] is None:
            book_info['borrowed_by'] = "Available"
        else:
            book_info['borrowed_by'] = "on loan"

        result.append(book_info)

    return result
    
def search_books(books, query):
    query=query.strip().casefold()

    if not query:
        return {
            "success": False,
            "message": "Search query cannot be empty.",
            "data": []
        }

    matches=[]
    for book in books:
        title=book['title'].casefold()
        author=book['author'].casefold()

        if query in title or query in author:
            book_info=book.copy()

            if book_info['borrowed_by'] is None:
                book_info['borrowed_by'] = "Available"  
            else:
                book_info['borrowed_by'] = "on loan"
            matches.append(book_info)

    return {
        "success": True,
        "message": (
            f"Found {len(matches)} book(s)"
            if matches 
            else "No books found."
        ),
        "data": matches
    }

def remove_book(books, book_id):
    book_id = book_id.strip()

    if not book_id:
        return {
            "success": False,
            "message": "Book ID is required.",
            "data": None
        }

    for index, book in enumerate(books):
        if book['book_id'] == book_id:
            if book['borrowed_by'] is not None:
                return {
                    "success": False,
                    "message": "Cannot remove a book that is on loan.",
                    "data": None
                }
            removed_book = books.pop(index)

            return {
                "success": True,
                "message": "Book removed successfully.",
                "data": removed_book
            }
    return {
        "success": False,
        "message": "Book not found.",
        "data": None
    }