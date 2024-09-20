import json

from api.models import Book


def handle_book_creation_message(ch, method, properties, body):
    message = json.loads(body)
    event = message["event"]
    data = message["data"]

    if event == "book_created":
        # Add book to frontend database
        Book.objects.create(
            title=data["title"],
            author=data["author"],
            publisher=data["publisher"],
            category=data["category"],
            created_at=data["created_at"],
            available=True,
        )
    elif event == "book_deleted":
        # Delete book from frontend database
        try:
            book = Book.objects.get(id=data["id"])
            book.delete()
        except Book.DoesNotExist:
            print(f"Book with ID {data['id']} does not exist")
