import unittest

from services.book_service import borrow_book, return_book

def setUp(self):

    self.books = [
        {
            "book_id": "B001",
            "title": "Python",
            "author": "John Smith",
            "borrowed_by": None
        },
        {
            "book_id": "B002",
            "title": "Python",
            "author": "John Smith",
            "borrowed_by": None
        },
        {
            "book_id": "B003",
            "title": "Java Basics",
            "author": "Jane Doe",
            "borrowed_by": "M001"
        },
        {
            "book_id": "B004",
            "title": "C++ Basics",
            "author": "Alex Lee",
            "borrowed_by": None
        }
    ]

    self.members = [
        {
            "member_id": "M001",
            "name": "Rahul",
            "borrowed_books": ["B003"]
        },
        {
            "member_id": "M002",
            "name": "Aisha Patel",
            "borrowed_books": []
        },
        {
            "member_id": "M003",
            "name": "Sanika",
            "borrowed_books": []
        }
    ]

def test_borrow_available_book(self):
    result = borrow_book(self.books, self.members, "M002", "B001")
    self.assertTrue(result["success"])
    self.assertEqual(self.books[0]["borrowed_by"], "M002")
    self.assertIn("B001", self.members[1]["borrowed_books"])

def test_borrow_already_borrowed_book(self):
    result = borrow_book(self.books, self.members, "M002", "B003")
    self.assertFalse(result["success"])
    self.assertEqual(self.books[2]["borrowed_by"], "M001")
    self.assertNotIn("B003", self.members[1]["borrowed_books"])

def test_borrow_nonexistent_book(self):
    result = borrow_book(self.books, self.members, "M002", "B999")
    self.assertFalse(result["success"])
    self.assertIsNone(self.books[1]["borrowed_by"])

def test_return_borrowed_book(self):
    result = return_book(self.books, self.members, "M001", "B003")
    self.assertTrue(result["success"])
    self.assertIsNone(self.books[2]["borrowed_by"])
    self.assertNotIn("B003", self.members[0]["borrowed_books"])

def test_return_book_not_borrowed_by_another_member(self):
    result = return_book(self.books, self.members, "M002", "B003")
    self.assertFalse(result["success"])
    self.assertEqual(self.books[2]["borrowed_by"], "M001")
    self.assertIn("B003", self.members[0]["borrowed_books"])

def test_return_nonexistent_book(self):
    result = return_book(self.books, self.members, "M002", "B999")
    self.assertFalse(result["success"])

def test_return_nonexistent_member(self):
    result = return_book(self.books, self.members, "M999", "B001")
    self.assertFalse(result["success"])
    self.assertIsNone(self.books[0]["borrowed_by"],"M001")

def test_borrow_another_copy_of_same_title(self):
    result = borrow_book(self.books, self.members, "M002", "B002")
    self.assertTrue(result["success"])
    self.assertEqual(self.books[1]["borrowed_by"], "M002")
    self.assertIsNone(self.members[1]["borrowed_books"].count("B002"))

if __name__ == '__main__':
    unittest.main()