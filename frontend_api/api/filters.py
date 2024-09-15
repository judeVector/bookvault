import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    publisher = django_filters.CharFilter(
        field_name="publisher", lookup_expr="icontains"
    )
    category = django_filters.CharFilter(field_name="category", lookup_expr="icontains")

    class Meta:
        model = Book
        fields = ["publisher", "category"]
