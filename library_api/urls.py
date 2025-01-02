from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    BookViewSet, register_user, CustomAuthToken, logout_user,
    CategoryViewSet, TransactionViewSet
)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
