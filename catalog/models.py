from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
from uuid import uuid4
from datetime import date

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (C/LN/AC)')

    def __str__(self):
        return self.name

class Book(models.Model):

    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    volume = models.IntegerField(null = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description ='Genre'

class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    class Meta:
        ordering =['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'

