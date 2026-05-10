from django.urls import path
from . import views

app_name = 'bills'

urlpatterns = [
    path('', views.bill_list_view, name='bill_list'),
    path('add/', views.bill_add_view, name='bill_add'),
    path('<int:pk>/edit/', views.bill_edit_view, name='bill_edit'),
    path('<int:pk>/delete/', views.bill_delete_view, name='bill_delete'),
]