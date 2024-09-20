import json

from api.models import User, Book, Borrow


def handle_user_creation_message(ch, method, properties, body):
    message = json.loads(body)
    event = message["event"]
    data = message["data"]

    if event == "user_created":
        User.objects.create(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            created_at=data["created_at"],
        )


def handle_borrow_message(ch, method, properties, body):
    message = json.loads(body)
    event = message["event"]
    data = message["data"]

    if event == "book_borrowed":
        user = User.objects.get(email=data["user"])
        book = Book.objects.get(title=data["book"])

        book.available = False
        book.save()

        Borrow.objects.create(
            user=user,
            book=book,
            borrow_date=data["borrow_date"],
            return_date=data["return_date"],
        )
