from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('expenses/', views.expense_list_view, name='expense_list'),
    path('expenses/add/', views.expense_add_view, name='expense_add'),
    path('expenses/<int:pk>/edit/', views.expense_edit_view, name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete_view, name='expense_delete'),
    path('income/', views.income_list_view, name='income_list'),
    path('income/add/', views.income_add_view, name='income_add'),
    path('income/<int:pk>/edit/', views.income_edit_view, name='income_edit'),
    path('income/<int:pk>/delete/', views.income_delete_view, name='income_delete'),
]