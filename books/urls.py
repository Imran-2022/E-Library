from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('add/',views.add_post,name='add_post'),
    path('book_details/<int:id>',views.book_details,name='book_details'),
    path('profile/',views.order_history,name='profile'),
    path('add_comment/<int:id>/', views.add_comment, name='add_comment'),
    path('borrow_now/',views.borrow_now,name='borrow_now'),
    path('edit/<int:id>',views.edit_post,name='edit_post'),
    path('delete/<int:id>',views.delete_post,name='delete_post')
]
