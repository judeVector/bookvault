from django.urls import path
from .views import (
    AdminBookCreateView,
    AdminBookDeleteView,
    AdminUserListView,
    AdminBorrowedBooksView,
)

urlpatterns = [
    path("books/", AdminBookCreateView.as_view(), name="admin-book-create"),
    path(
        "books/<int:pk>/delete/",
        AdminBookDeleteView.as_view(),
        name="admin-book-delete",
    ),
    path("users/", AdminUserListView.as_view(), name="admin-user-list"),
    path(
        "books/borrowed/", AdminBorrowedBooksView.as_view(), name="admin-borrowed-books"
    ),
]
