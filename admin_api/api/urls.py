from django.urls import path
from .views import (
    AdminBookCreateView,
    AdminBookDeleteView,
    AdminUserListView,
    UserBorrowedBooksListView,
    UnavailableBooksListView,
)

urlpatterns = [
    path("books/", AdminBookCreateView.as_view(), name="admin-book-create"),
    path(
        "books/<int:pk>/delete/",
        AdminBookDeleteView.as_view(),
        name="admin-book-delete",
    ),
    path("users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("borrowed/", UserBorrowedBooksListView.as_view(), name="borrowed-books"),
    path("unavailable/", UnavailableBooksListView.as_view(), name="unavailable-books"),
]
