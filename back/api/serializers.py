from rest_framework import serializers
from .models import Category, Book, Review, BookShelf, Comment
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

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.get(id=category_data['id'])
        return Book.objects.create(category=category, **validated_data)

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
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ['id', 'book', 'user', 'rating', 'comment']


class BookShelfSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BookShelf
        fields = ['id', 'name', 'user', 'books']

class CommentSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'content', 'date']

