from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import CategorySerializer, BookSerializer, ReviewSerializer, BookShelfSerializer, CommentSerializer, UserSerializer, SavedBookSerializer
from .models import Category, Book, Review, BookShelf, Comment, SavedBook
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import pandas as pd
from rest_framework.renderers import JSONRenderer

renderer_classes = [JSONRenderer,]

User = get_user_model()

@csrf_exempt
def post_books(request):
    import json

    books = []

    with open('api/importing/booksDataset.json') as f:
        data = json.load(f)

    for book in data:
        book = Book.objects.create(
            title=book['title'],
            author=book['author'],
            year=book['year'],
            publisher=book['publisher'],
            image=book['image'],
            category=Category.objects.get(name=book['category']),
            description=book['description'],
            rating=book['rating'],
            likes=book['likes'],
            link=book['link']
        )
        books.append(book)

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json')

def load_books_from_excel(request):
    df = pd.read_excel('api/importing/booksDataset.xlsx')

    for index, row in df.iterrows():
        category, _ = Category.objects.get_or_create(name=row['category'])

        book = Book(
            title=row['title'],
            author=row['author'],
            year=row['year'],
            publisher=row['publisher'],
            image=row['image'],
            category=category,  # использовать объект Category, полученный выше
            description=row['description'],
            rating=row['rating'],
            likes=row['likes'],
            link=row['link']
        )
        book.save()

    return Response('Books loaded successfully.')

@csrf_exempt
@api_view(['GET'])
def get_user(request):
    if request.method == 'GET':        
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        # Check if the email or username already exists in the database
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists.'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'})

        # Create the new user object
        user = User.objects.create_user(username=username, email=email, password=password)

        # Return a success message
        return JsonResponse({'success': 'User registered successfully.'})
    
# Category views
@csrf_exempt
@api_view(['GET', 'POST'])
def get_categories(request): 
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def get_category(request, id): 
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist as error:
        return Response({'error': str(error)}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response({'deleted': True}, status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET'])
def get_category_books(request, id):
    if request.method == 'GET':
        needed_category = Category.objects.get(id=id)
        books = Book.objects.filter(category=needed_category)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_books_comments(request, id):
    if request.method == 'GET':
        book = Book.objects.get(id=id)
        comments = Comment.objects.filter(book=book)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@csrf_exempt
@api_view(['GET'])
def get_book_by_review(request, review_id):
    review = Review.objects.get(id=review_id)
    book = review.book
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_books_reviews(request, id):
    if request.method == 'GET':
        book = Book.objects.get(id=id)
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Books views 
class BooksAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailAPIView(APIView):
    def get_book(self, id):
        try: 
            return Book.objects.get(id=id)
        except Book.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        
    def get(self, request, id):
        book = self.get_book(id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        book = self.get_book(id)
        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        book = self.get_book(id)
        book.delete()
        return Response({'deleted': True}, status=status.HTTP_204_NO_CONTENT)

# Review views 
class ReviewListAPIView(ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
   
class ReviewRetrieveAPIView(RetrieveAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

class ReviewCreateAPIView(CreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewUpdateAPIView(UpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

class ReviewDeleteAPIView(DestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

class UserReviewsListAPIView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


# Saved book views
class SavedBookCreateViews(CreateAPIView):
    serializer_class = SavedBookSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@csrf_exempt
@api_view(['GET'])
def get_users_saved_books(request):
    saved_books = SavedBook.objects.filter(user=request.user)
    serializer = SavedBookSerializer(saved_books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class SavedBookDeleteView(DestroyAPIView):
    serializer_class = SavedBookSerializer
    queryset = SavedBook.objects.all() 
    lookup_field = 'id'    

# BookShelf views

# View for creating a new BookShelf:
class BookShelfCreateView(CreateAPIView):
    serializer_class = BookShelfSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# View for retrieving a specific BookShelf:
class BookShelfDetailView(RetrieveAPIView):
    serializer_class = BookShelfSerializer
    queryset = BookShelf.objects.all()

# View for updating an existing BookShelf:
class BookShelfUpdateView(UpdateAPIView):
    serializer_class = BookShelfSerializer
    queryset = BookShelf.objects.all()

# View for deleting an existing BookShelf:
class BookShelfDeleteView(DestroyAPIView):
    serializer_class = BookShelfSerializer
    queryset = BookShelf.objects.all()

# View for listing all BookShelfs owned by a specific user:
class BookShelfListView(ListAPIView):
    serializer_class = BookShelfSerializer

    def get_queryset(self):
        return BookShelf.objects.filter(user=self.request.user)


# Comments views 
# List all comments
class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

# Retrieve a specific comment by ID
class CommentRetrieveAPIView(RetrieveAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'

# Create a new comment
class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Update an existing comment
class CommentUpdateAPIView(UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'
    # lookup_url_kwarg = "id"

# Delete an existing comment
class CommentDeleteAPIView(DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'    

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
@csrf_exempt 
@api_view(['GET']) 
@permission_classes([AllowAny])
def get_user(request): 
    user = request.user 
    serializer = UserSerializer(user) 
    return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def get_books_by_author(request, author):
    books = Book.objects.get_books_by_author(author)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET'])
def get_books_by_publisher(request, publisher):
    books = Book.objects.get_books_by_publisher(publisher)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

