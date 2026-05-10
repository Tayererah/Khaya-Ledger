from django.urls import path
from . import views

app_name = 'savings'

urlpatterns = [
    path('', views.savings_list_view, name='savings_list'),
    path('add/', views.savings_add_view, name='savings_add'),
    path('<int:pk>/edit/', views.savings_edit_view, name='savings_edit'),
    path('<int:pk>/delete/', views.savings_delete_view, name='savings_delete'),
]