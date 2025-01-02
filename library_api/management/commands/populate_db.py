from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library_api.models import Category, Book
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate database with sample books and categories'

    def handle(self, *args, **kwargs):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))

        # Create categories
        categories_data = [
            {
                'name': 'Fiction',
                'description': 'Fictional literature and novels'
            },
            {
                'name': 'Science',
                'description': 'Scientific books and research papers'
            },
            {
                'name': 'History',
                'description': 'Historical books and documentaries'
            },
            {
                'name': 'Technology',
                'description': 'Books about computers, programming, and technology'
            },
            {
                'name': 'Philosophy',
                'description': 'Books about philosophical thoughts and theories'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create books
        books_data = [
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'category': 'Fiction',
                'publication_date': '1949-06-08',
                'description': 'A dystopian novel about totalitarianism',
                'quantity': 5
            },
            {
                'title': 'A Brief History of Time',
                'author': 'Stephen Hawking',
                'isbn': '9780553380163',
                'category': 'Science',
                'publication_date': '1988-03-01',
                'description': 'A book about modern physics for non-scientists',
                'quantity': 3
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'isbn': '9780132350884',
                'category': 'Technology',
                'publication_date': '2008-08-11',
                'description': 'A handbook of agile software craftsmanship',
                'quantity': 7
            },
            {
                'title': 'The Republic',
                'author': 'Plato',
                'isbn': '9780872201361',
                'category': 'Philosophy',
                'publication_date': '1992-03-01',
                'description': 'A Socratic dialogue about justice and the order of a just city-state',
                'quantity': 4
            },
            {
                'title': 'Sapiens',
                'author': 'Yuval Noah Harari',
                'isbn': '9780062316097',
                'category': 'History',
                'publication_date': '2014-02-10',
                'description': 'A brief history of humankind',
                'quantity': 6
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt, David Thomas',
                'isbn': '9780201616224',
                'category': 'Technology',
                'publication_date': '1999-10-20',
                'description': 'From journeyman to master',
                'quantity': 4
            },
            {
                'title': 'Dune',
                'author': 'Frank Herbert',
                'isbn': '9780441172719',
                'category': 'Fiction',
                'publication_date': '1965-08-01',
                'description': 'A science fiction masterpiece',
                'quantity': 8
            }
        ]

        admin_user = User.objects.get(username='admin')
        
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={
                    'title': book_data['title'],
                    'author': book_data['author'],
                    'category': categories[book_data['category']],
                    'publication_date': datetime.strptime(book_data['publication_date'], '%Y-%m-%d').date(),
                    'description': book_data['description'],
                    'quantity': book_data['quantity'],
                    'available': book_data['quantity'],
                    'added_by': admin_user
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
