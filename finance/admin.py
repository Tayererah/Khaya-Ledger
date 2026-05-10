from django.contrib import admin
from .models import Category, Income, Expense

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'household']
    list_filter = ['category_type']
    search_fields = ['name']

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['source', 'amount', 'member', 'date', 'is_recurring']
    list_filter = ['is_recurring', 'date']
    search_fields = ['source']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['description', 'amount', 'category', 'member', 'date']
    list_filter = ['category', 'date']
    search_fields = ['description']
