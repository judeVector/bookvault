from rest_framework import generics

from .models import AdminBook, User
from .serializers import AdminBookSerializer, UserSerializer


class AdminBookCreateView(generics.CreateAPIView):
    queryset = AdminBook.objects.all()
    serializer_class = AdminBookSerializer


class AdminBookDeleteView(generics.DestroyAPIView):
    queryset = AdminBook.objects.all()
    serializer_class = AdminBookSerializer


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AdminBorrowedBooksView(generics.ListAPIView):
    queryset = AdminBook.objects.filter(available=False)
    serializer_class = AdminBookSerializer
