from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import CategorySerializer, BookSerializer, ReviewSerializer, BookShelfSerializer, CommentSerializer
from .models import Category, Book, Review, BookShelf, Comment
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

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

class ReviewUpdateAPIView(UpdateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

class ReviewDeleteAPIView(DestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
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

# Update an existing comment
class CommentUpdateAPIView(UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'

# Delete an existing comment
class CommentDeleteAPIView(DestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'    

# class CommentList(APIView):
#     """
#     Выводит список всех комментариев к книге, либо создает новый комментарий.
#     """
#     def get(self, request, book_id):
#         comments = Comment.objects.filter(book=book_id)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)

#     def post(self, request, book_id):
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user, book_id=book_id)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
