import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, username, and password.
        """
        if not email:
            raise ValueError('The Email field must be set.')
        if not username:
            raise ValueError('The Username field must be set.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='api_user_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='api_user_permissions'
    )
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     password = models.CharField(max_length=128)
    
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         related_name='api_user_groups'
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         related_name='api_user_permissions'
#     )
    
#     USERNAME_FIELD = 'username'

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    class Meta: 
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.id}: {self.name}'
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


class BookManager(models.Manager):
    def get_books_by_author(self, author):
        return self.filter(author=author)
    
    def get_books_by_publisher(self, publisher):
        return self.filter(publisher=publisher)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    year = models.IntegerField()
    publisher = models.CharField(max_length=255)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.FloatField(default=0)
    objects = BookManager()


    class Meta: 
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f'{self.id}: {self.title}, {self.year}, {self.publisher}, {self.description}, {self.author}, {self.category}, {self.rating}'
    
    def to_json(self):
        return {
            'id': self.id, 
            'title': self.title, 
            'author': self.author,
            'description': self.description, 
            'image': self.image, 
            'category': self.category.to_json()
        }

# "Review" - модель для отзывов, которые пользователи могут оставлять о книгах.

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)    
    rating = models.IntegerField()
    comment = models.TextField()
    # date = models.DateField(default=timezone.now, null=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
         
    def __str__(self):
        return f'Review #{self.id}, {self.book}, {self.user.username}, {self.rating}, {self.comment}'

    def to_json(self):
        return {
            'id': self.id,
            'book': self.book.title,
            'user': self.user.username,
            'rating': self.rating,
            'comment': self.comment
        }

# "BookShelf" - модель для книжных полок, которые пользователи могут 
# создавать и управлять ими, добавляя книги в избранное, 
# читаемое, прочитанное и т.д.
class BookShelf(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)    
    books = models.ManyToManyField(Book)

    class Meta:
        verbose_name = 'Bookshelf'
        verbose_name_plural = 'Bookshelfs'

    def __str__(self):
        return f'Bookshelf #{self.id}, {self.name}, {self.user.username}, {self.books}'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user': self.user.username,
            'books': list(self.books.values_list('id', flat=True)),
        }

# "Comment" - модель для комментариев, которые пользователи 
# могут оставлять на страницах книг или отзывов.
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)    
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment #{self.id}, {self.book}, {self.user.username}, {self.content}, {self.date}'

    def to_json(self):
        return {
            'id': self.id,
            'book': self.book.title,
            'user': self.user.username,
            'content': self.content,
            'date': self.date.isoformat(),
        } 
