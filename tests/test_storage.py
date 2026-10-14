import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from storage.storage import load_data


def test_load_library_data():
    data = load_data()
    books = data["books"]
    members = data["members"]

    assert len(books) == 11
    assert len(members) == 4
    assert all(
        set(book) == {"book_id", "title", "author", "borrowed_by"}
        for book in books
    )
    assert all(
        set(member) == {"member_id", "name", "borrowed_books"}
        for member in members
    )
    assert len({book["book_id"] for book in books}) == len(books)
    assert len({member["member_id"] for member in members}) == len(members)

    print(f"Loaded {len(books)} books and {len(members)} members from library.json")


if __name__ == "__main__":
    test_load_library_data()
