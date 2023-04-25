from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User , AbstractUser
 
User= get_user_model()

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


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    year = models.IntegerField()
    publisher = models.CharField(max_length=255)
    image = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.FloatField(default=0)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

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
            'comment': self.comment,
        }

# "BookShelf" - модель для книжных полок, которые пользователи могут 
# создавать и управлять ими, добавляя книги в избранное, 
# читаемое, прочитанное и т.д.
class BookShelf(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
