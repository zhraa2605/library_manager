from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from typing import Any

from .models import Book, UserProfile, Category, Transaction
from .serializers import (
    BookSerializer, UserSerializer, CategorySerializer,
    TransactionSerializer
)

class IsLibraryStaff(permissions.BasePermission):
    """Permission class for library staff (admin and librarian)."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff

class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset with common functionality."""
    permission_classes = [permissions.IsAuthenticated]

class CategoryViewSet(BaseViewSet):
    """ViewSet for managing book categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsLibraryStaff]

class BookViewSet(BaseViewSet):
    """ViewSet for managing books and their transactions."""
    queryset = Book.objects.select_related('category', 'added_by').all()
    serializer_class = BookSerializer
    permission_classes = [IsLibraryStaff]
    
    def get_queryset(self):
        """Filter books based on query parameters."""
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        available = self.request.query_params.get('available')
        
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        if available:
            queryset = queryset.filter(available__gt=0)
            
        return queryset

    def perform_create(self, serializer):
        """Set the user who added the book."""
        serializer.save(added_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def borrow(self, request, pk=None):
        """Borrow a book."""
        book = self.get_object()
        due_date = request.data.get('due_date') or (
            timezone.now() + timedelta(days=14)
        )
        
        serializer = TransactionSerializer(data={
            'book': book.id,
            'user': request.user.id,
            'transaction_type': Transaction.BORROW,
            'due_date': due_date,
            'notes': request.data.get('notes', '')
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def return_book(self, request, pk=None):
        """Return a borrowed book."""
        book = self.get_object()
        
        serializer = TransactionSerializer(data={
            'book': book.id,
            'user': request.user.id,
            'transaction_type': Transaction.RETURN,
            'notes': request.data.get('notes', '')
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TransactionViewSet(BaseViewSet):
    """ViewSet for managing book transactions."""
    serializer_class = TransactionSerializer

    def get_queryset(self):
        """Filter transactions based on user role."""
        if self.request.user.is_staff:
            return Transaction.objects.select_related('book', 'user').all()
        return Transaction.objects.select_related('book', 'user').filter(
            user=self.request.user
        )

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """List overdue transactions."""
        queryset = self.get_queryset().filter(
            transaction_type=Transaction.BORROW,
            returned_date__isnull=True,
            due_date__lt=timezone.now()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """Register a new user."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        if not request.user.is_superuser:
            serializer.validated_data['user_type'] = UserProfile.CUSTOMER
            
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'address': user.profile.address,
            'user_type': user.profile.user_type
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    """Custom token authentication view."""
    
    def post(self, request, *args, **kwargs):
        """Handle user login and return token with user data."""
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'address': user.profile.address,
            'user_type': user.profile.user_type
        })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_user(request):
    """Handle user logout."""
    request.user.auth_token.delete()
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
