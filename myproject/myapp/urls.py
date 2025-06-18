from django.urls import path, include
from .views import BookListCreate, BookDeatail, Register

urlpatterns = [
    path('books/', BookListCreate.as_view(), name="book-list-create"),
    path('books/<int:pk>/', BookDeatail.as_view(), name="book-detail"),
    path('register/', Register.as_view(), name="register"),
    # path('user/', include('rest_framework.urls', namespace='rest_framework')),
]