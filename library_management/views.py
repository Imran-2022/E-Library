from django.shortcuts import render
from books.models import Books
from Categories.models import Category
# Create your views here.

def home(request,category_slug=None):
    data = Books.objects.all()
    # print(data)
    if category_slug is not None:
        category=Category.objects.get(slug=category_slug)
        data = Books.objects.filter(category=category)

    categories=Category.objects.all()
    return render(request,'home.html',{'data':data,'category':categories})
