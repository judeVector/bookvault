from django.urls import path
from .views import (
    AdminBookCreateView,
    AdminBookDeleteView,
    AdminUserListView,
    UserBorrowedBooksListView,
    UnavailableBooksListView,
)

urlpatterns = [
    path("books/", AdminBookCreateView.as_view(), name="admin_book_create"),
    path(
        "books/<int:pk>/delete/",
        AdminBookDeleteView.as_view(),
        name="admin_book_delete",
    ),
    path("users/", AdminUserListView.as_view(), name="admin_user_list"),
    path("borrowed/", UserBorrowedBooksListView.as_view(), name="borrowed_books"),
    path("unavailable/", UnavailableBooksListView.as_view(), name="unavailable_books"),
]
