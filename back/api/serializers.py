from rest_framework import serializers
from .models import Category, Book, Review, Bookshelf, Comment
from django.contrib.auth.models import User


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=50)
    year = serializers.IntegerField()
    publisher = serializers.CharField(max_length=255)
    image = serializers.URLField()
    category = CategorySerializer()
    description = serializers.CharField()
    rating = serializers.FloatField()
    link = serializers.URLField()

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category_id = category_data.pop('id', None)
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
        if not category:
            category = Category.objects.create(**category_data)

        title = validated_data['title']
        author = validated_data['author']
        existing_book = Book.objects.filter(title=title, author=author).first()
        if existing_book:
            book = existing_book
            # Add the category in case it wasn't already associated with the book
            if not book.category:
                book.category = category
                book.save()
        else:
            validated_data['category'] = category
            book = Book.objects.create(**validated_data)
        return book

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.get(id=category_data['id'])
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.year = validated_data.get('year', instance.year)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.image = validated_data.get('image', instance.image)
        instance.category = category
        instance.description = validated_data.get('description', instance.description)
        instance.rating = validated_data.get('rating', instance.rating)
        # instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance

class BookshelfSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True,read_only=True)
    class Meta:
        model = Bookshelf
        fields = ['id', 'name','books']
        read_only_fields = ['books']
    # def create(self, validated_data):
    #     books_data = validated_data.pop('books', [])
    #     bookshelf = Bookshelf.objects.create(**validated_data)
    #     for book_data in books_data:
    #         book_id = book_data.pop('id', None) # Extract the id field from book_data
    #         book = None
    #         if book_id:
    #             try:
    #                 book = Book.objects.get(id=book_id) # Search for the Book object with the extracted id
    #             except Book.DoesNotExist:
    #                 pass
    #         if not book:
    #             book = Book.objects.create(bookshelf=bookshelf, **book_data)
    #         bookshelf.books.add(book) # Add the Book object to the books field of the created Bookshelf object
    #     return bookshelf

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name']


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'username', 'rating', 'comment', 'date']



class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'username', 'content', 'date']
