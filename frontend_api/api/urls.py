from django.urls import path

from api.views import (
    UserCreateView,
    BookListView,
    BookDetailView,
    BorrowBookView,
    CreateBookView,
)

urlpatterns = [
    path("users/", UserCreateView.as_view(), name="user-create"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:book_id>/borrow/", BorrowBookView.as_view(), name="book-borrow"),
    path("books/create/", CreateBookView.as_view(), name="create_book"),
]
