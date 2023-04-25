from django.urls import path
from api import views

urlpatterns = [
    path('categories/', views.get_categories),
    path('categories/<int:id>', views.get_category),
    path('categories/<int:id>/books', views.get_category_books),
    path('books/', views.BooksAPIView.as_view()),
    path('books/<int:id>', views.BookDetailAPIView.as_view()), 
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('comments/', views.CommentListAPIView.as_view()),
    path('books/<int:id>/comments/', views.get_books_comments),
    path('books/<int:id>/reviews/', views.get_books_reviews),
]