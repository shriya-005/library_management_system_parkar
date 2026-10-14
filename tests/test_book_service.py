import unittest

from services.book_service import (
    add_book, 
    display_book,
    search_books,
    remove_book,
)

class TestBookService(unittest.TestCase):
    def setUp(self):
        self.books = [
            {
                "book_id": "B001",
                "title": "Python Basics",
                "author": "John Smith",
                "borrowed_by": None
            },
            {
                "book_id": "B002",
                "title": "Good girl's guide to murder",
                "author": "Holly Jackson",
                "borrowed_by": None
            },
            {
                "book_id": "B003",
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "borrowed_by": None
            },
            {
                "book_id":"B004",
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "borrowed_by": None
            },
            {
                "book_id": "B005",
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "borrowed_by": None
            },
        ]

def test_add_book(self):
    result=(
        self.books, "B006","Harry Potter","J.K. Rowling"
    )

    self.assertTrue(result["success"])
    self.assertEqual(len(self.books), 6)

def test_add_duplicate_book_id(self):
    result = add_book(
        self.books, "B001", "Another Book", "Author Name"
    )
    self.assertFalse(result["success"])
    self.assertEqual(len(self.books), 5)

def test_add_book_with_empty_title(self):
    result = add_book(
        self.books, "B006", "", "J.K. Rowling"
    )
    self.assertFalse(result["success"])
    self.assertEqual(len(self.books), 5)

def test_display_books(self):
    result = display_book(self.books)
    self.assertEqual(len(result["data"]), 5)

def test_display_empty_collection(self):
    result = display_book([])
    self.assertTrue(result["success"])
    self.assertEqual(len(result["data"]), [])

def test_search_by_title(self):
    result = search_books(self.books, "Pride and Prejudice")
    self.assertEqual(len(result["data"]), 1)
    self.assertEqual(
        result["data"][0]["book_id"], "B003"
    )

def test_search_by_author(self):
    result = search_books(self.books, "Holly Jackson")
    self.assertEqual(len(result["data"]), 1)
    self.assertEqual(
        result["data"][0]["book_id"], "B002"
    )

def test_search_ignore_case(self):
    result = search_books(self.books, "python basics")
    self.assertEqual(len(result["data"]), 1)
    self.assertEqual(
        result["data"][0]["book_id"], "B001"
    )

def test_search_by_partial_title(self):
    result = search_books(self.books, "mockingbird")
    self.assertEqual(len(result["data"]), 1)
    self.assertEqual(
        result["data"][0]["book_id"], "B004"
    )

def test_search_by_partial_author(self):
    result = search_books(self.books, "austen")
    self.assertEqual(len(result["data"]), 1)
    self.assertEqual(
        result["data"][0]["book_id"], "B003"
    )

def test_search_no_results(self):
    result = search_books(self.books, "xyz123")

    self.assertTrue(result["success"])
    self.assertEqual(result["data"], [])

def test_search_empty_query(self):
    result = search_books(self.books, "")
    self.assertFalse(result["success"])

def test_remove_book(self):
    result = remove_book(self.books, "B001")
    self.assertTrue(result["success"])
    self.assertEqual(len(self.books), 4)

def test_cannot_remove_book_on_loan(self):
    self.books[0]["borrowed_by"] = "M001"
    result = remove_book(self.books, "B001")
    self.assertFalse(result["success"])
    self.assertEqual(len(self.books), 5)

def test_remove_nonexistent_book(self):
    result = remove_book(self.books, "B999")
    self.assertFalse(result["success"])
    self.assertEqual(len(self.books), 5)

if __name__ == "__main__":
    unittest.main(verbosity=2)