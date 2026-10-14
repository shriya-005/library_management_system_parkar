from storage.storage import load_data, save_data
books=[
    {
        "book_id":" B001",
        "title":"Python Basics",
        "author":"F. John Smith",
        "borrowed_by":None  
    }
]
members=[
    {
        "member_id":"M001", 
        "name":"Rahul",
        "borrowed_books":[]

    }
]
save_data(books, members)
print(load_data())
