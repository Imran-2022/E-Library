from django.shortcuts import render,redirect
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Books,Order,Comment
from django.contrib import messages
# Create your views here.

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
def borrow_now(request):
    if request.method == 'POST' and request.user.is_authenticated:
        Book_id = request.POST.get('book_id')
        if Book_id:
            # Get the Book object
            Book = Books.objects.get(id=Book_id)
            # Create a new order for the current user
            Order.objects.create(book=Book, user=request.user)  # Change 'Book' to 'book'
            # Decrease the Book quantity
            Book.quantity_available -= 1  # Update the field name to 'quantity_available'
            Book.save()
    return redirect('profile')  # Redirect to order history page or user profile

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    print(context)
    return render(request, 'profile.html', context)


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
