# books/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import Book

def list_books(request):
    search_query = request.GET.get('search', '')
    if search_query:
        books = Book.objects.filter(title__icontains=search_query)
    else:
        books = Book.objects.all()
    context = {
        'books': books,
        'search_query': search_query
    }
    return render(request, 'list_books.html', context)

def add_book(request):
    error = None
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        published_date = request.POST.get('published_date', '').strip()
        summary = request.POST.get('summary', '').strip()

        # Validate required fields.
        if not title or not author:
            error = "Title and Author are required."
        else:
            try:
                Book.objects.create(
                    title=title,
                    author=author,
                    published_date=published_date,
                    summary=summary
                )
                return redirect('list_books')
            except IntegrityError:
                error = "A book with this title already exists."
    return render(request, 'add_book.html', {'error': error})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    error = None
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        published_date = request.POST.get('published_date', '').strip()
        summary = request.POST.get('summary', '').strip()

        if not title or not author:
            error = "Title and Author are required."
        else:
            # Check for duplicate title in other records.
            if Book.objects.exclude(id=book_id).filter(title=title).exists():
                error = "Another book with this title already exists."
            else:
                book.title = title
                book.author = author
                book.published_date = published_date
                book.summary = summary
                book.save()
                return redirect('list_books')
    return render(request, 'edit_book.html', {'book': book, 'error': error})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'delete_book.html', {'book': book})
