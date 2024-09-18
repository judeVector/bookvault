from django.contrib import admin

from .models import User, Book, Borrow, AdminBook

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(AdminBook)
