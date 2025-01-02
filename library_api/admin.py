from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Category, Book, Transaction, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'is_staff', 'get_user_type')
    
    def get_user_type(self, obj):
        return obj.profile.user_type if hasattr(obj, 'profile') else '-'
    get_user_type.short_description = 'User Type'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'quantity', 'available')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author', 'isbn')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'transaction_type', 'transaction_date', 'due_date', 'returned_date')
    list_filter = ('transaction_type', 'created_at', 'due_date')
    search_fields = ('book__title', 'user__username')

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)