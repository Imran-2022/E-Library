from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Books,Order,Comment
from django.contrib import messages
# Create your views here.
from accounts.models import Account  # Import Account model
from django.utils import timezone
from decimal import Decimal
# books/views.py
from .forms import ReviewForm  # Import ReviewForm
@login_required
def add_comment(request, id):
    if request.method == 'POST':
        book = Books.objects.get(pk=id)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            comment_text = review_form.cleaned_data['comment']
            Comment.objects.create(book=book, user=request.user, comment=comment_text)
            messages.success(request, 'Review added successfully!')
            return redirect('book_details', id=id)
    else:
        review_form = ReviewForm()
    return render(request, 'book_details.html', {'book': book, 'review_form': review_form})

@login_required
def return_book(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    book = order.book
    account, created = Account.objects.get_or_create(user=request.user)
    
    # Update the book's availability
    book.quantity_available += 1
    book.save()
    
    # Refund the user
    account.balance += book.borrow_price
    account.save()
    
    # Update the order with the return date
    order.return_date = timezone.now()
    order.save()
    # Delete the order to remove the book from the borrowed list
    order.delete()

    messages.success(request, 'Book returned successfully!')
    return redirect('profile')

@login_required
def borrow_now(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        if book_id:
            try:
                book = Books.objects.get(id=book_id)
                account, created = Account.objects.get_or_create(user=request.user)
                
                # Ensure borrow_price is a Decimal
                borrow_price = Decimal(book.borrow_price)
                if account.balance >= borrow_price:
                    # Create an order
                    Order.objects.create(book=book, user=request.user)
                    
                    # Deduct the borrow price from the user's balance
                    # Refund the user
                    account.balance -= book.borrow_price
                    account.save()

                    messages.success(request, 'Book borrowed successfully!')
                else:
                    messages.warning(request, 'Insufficient balance!')
            
            except Books.DoesNotExist:
                messages.error(request, 'Book not found!')
    
    return redirect('profile')

@login_required
def add_post(request):
    if request.method=='POST':
        post_form=forms.PostForm(request.POST)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)  # Create a new Post object but don't save to database yet
            new_post.author = request.user  # Assign the author
            new_post.save()  # Save the post with the assigned author
            return redirect('add_post')
    else:
        post_form=forms.PostForm()
    return render(request, 'add_post.html',{'form':post_form})

@login_required
def edit_post(request,id):
    # post model er instance (/object/children) dakhte parbe ! 

    post=models.Post.objects.get(pk=id)
    # print(post)
    post_form=forms.PostForm(instance=post)

    if request.method=='POST':
        post_form=forms.PostForm(request.POST,instance=post)
        # user kno kichu change na krle instance... !
        if post_form.is_valid():
            post_form.instance.author=request.user
            post_form.save()
            return redirect('homepage')
    return render(request, 'add_post.html',{'form':post_form})


def book_details(request, id):
    post = get_object_or_404(Books, pk=id)
    return render(request, 'book_details.html', {'book': post})

@login_required
def delete_post(request,id):
    post=models.Post.objects.get(pk=id)
    post.delete()
    return redirect('homepage')

@login_required
def add_comment(request, id):
    if request.method == 'POST':
        book = Books.objects.get(pk=id)  # Change 'Book' to 'book'
        name = request.POST['name']
        comment_text = request.POST['comment']
        Comment.objects.create(book=book, user=request.user, name=name, comment=comment_text)  # Change 'Book' to 'book'
        messages.success(request, 'Comment added successfully!')
        return redirect('book_details', id=id)  # Redirect to book details using 'id' parameter
    else:
        return redirect('homepage')  # Redirect to home page if not a POST request

@login_required
def profile(request):
    account = Account.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user)
    context = {
        'account': account,
        'orders': orders,
    }
    print(context)
    return render(request, 'profile.html', context)
