from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    
    path('dashboard/', views.home, name='home'),
    
    
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/update/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    
    path('members/', views.member_list, name='member_list'),
    path('members/create/', views.member_create, name='member_create'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    path('members/<int:pk>/update/', views.member_update, name='member_update'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'), 
    path('employees/<int:pk>/update/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    
    path('borrowing/', views.borrowing_list, name='borrowing_list'),
    path('borrowing/create/', views.borrowing_create, name='borrowing_create'),
    path('borrowing/<int:pk>/', views.borrowing_detail, name='borrowing_detail'),
    path('borrowing/<int:pk>/update/', views.borrowing_update, name='borrowing_update'),
    path('borrowing/<int:pk>/delete/', views.borrowing_delete, name='borrowing_delete'),
]
