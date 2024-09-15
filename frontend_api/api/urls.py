from django.urls import path

from .views import BookListView, BookDetailView, BorrowBookView

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/borrow/", BorrowBookView.as_view(), name="book-borrow"),
]
