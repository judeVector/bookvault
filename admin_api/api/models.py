from django.db import models

# Create your models here.


class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.email


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class AdminBook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    borrowed_until = models.DateField(null=True, blank=True)
