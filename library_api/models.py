from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from typing import Any

class BaseModel(models.Model):
    """Base model with common fields and methods."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    """Model for book categories."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

class Book(BaseModel):
    """Model for books in the library."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name='books',
        null=True
    )
    publication_date = models.DateField()
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    added_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='added_books'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['title']),
        ]

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        if self.available > self.quantity:
            raise ValidationError({
                "available": "Available books cannot exceed total quantity"
            })

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.clean()
        super().save(*args, **kwargs)

class Transaction(BaseModel):
    """Model for book borrowing transactions."""
    BORROW = 'borrow'
    RETURN = 'return'
    TRANSACTION_TYPES = [
        (BORROW, 'Borrow'),
        (RETURN, 'Return'),
    ]

    book = models.ForeignKey(
        Book, 
        on_delete=models.PROTECT, 
        related_name='transactions'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='transactions'
    )
    transaction_type = models.CharField(
        max_length=10, 
        choices=TRANSACTION_TYPES
    )
    transaction_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_type']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self) -> str:
        return f"{self.get_transaction_type_display()} - {self.book.title}"

    def clean(self) -> None:
        if self.transaction_type == self.BORROW:
            self._validate_borrow()
        elif self.transaction_type == self.RETURN:
            self._validate_return()

    def _validate_borrow(self) -> None:
        if self.book.available < 1:
            raise ValidationError({
                "book": "Book is not available for borrowing"
            })
        if not self.due_date:
            raise ValidationError({
                "due_date": "Due date is required for borrowing"
            })
        if self.due_date <= timezone.now():
            raise ValidationError({
                "due_date": "Due date must be in the future"
            })

    def _validate_return(self) -> None:
        if not Transaction.objects.filter(
            book=self.book,
            user=self.user,
            transaction_type=self.BORROW,
            returned_date__isnull=True
        ).exists():
            raise ValidationError({
                "transaction_type": "No matching borrow record found"
            })

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.clean()
        if self.transaction_type == self.BORROW:
            self.book.available -= 1
        elif self.transaction_type == self.RETURN:
            self.book.available += 1
            self.returned_date = timezone.now()
        self.book.save()
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    """Model for storing additional user information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=[('librarian', 'Librarian'), ('member', 'Member')], default='member')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.user_type == 'librarian':
            self.user.is_staff = True
        else:
            self.user.is_staff = False
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Create or update user profile when user is created/updated."""
    if created:
        UserProfile.objects.create(user=instance)
