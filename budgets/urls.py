from django.urls import path
from . import views

app_name = 'budgets'

urlpatterns = [
    path('', views.budget_list_view, name='budget_list'),
    path('add/', views.budget_add_view, name='budget_add'),
    path('<int:pk>/edit/', views.budget_edit_view, name='budget_edit'),
    path('<int:pk>/delete/', views.budget_delete_view, name='budget_delete'),
]