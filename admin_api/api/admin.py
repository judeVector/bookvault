from django.contrib import admin

from .models import User, Book, AdminBook

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(AdminBook)
