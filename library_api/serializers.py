from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Book, Transaction, UserProfile

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'book_count']


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    status = serializers.CharField(read_only=True)
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'category', 'category_name',
            'publication_date', 'description', 'quantity', 'available',
            'status', 'added_by', 'added_by_username'
        ]
        read_only_fields = ['available', 'added_by']

    def validate_isbn(self, value):
        """Validate ISBN format."""
        if not value.isdigit() or len(value) != 13:
            raise serializers.ValidationError(
                "ISBN must be a 13-digit number"
            )
        return value


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for the Transaction model."""
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'book', 'book_title', 'user', 'user_username',
            'transaction_type', 'transaction_date', 'due_date',
            'return_date', 'status'
        ]
        read_only_fields = ['transaction_date', 'return_date']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model."""
    class Meta:
        model = UserProfile
        fields = ['user_type']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model with profile information."""
    profile = UserProfileSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        read_only_fields = ['id']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
            
        return super().update(instance, validated_data)
