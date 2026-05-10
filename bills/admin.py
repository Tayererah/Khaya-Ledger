from django.contrib import admin
from .models import Bill, BillPayment

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'due_day', 'household', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(BillPayment)
class BillPaymentAdmin(admin.ModelAdmin):
    list_display = ['bill', 'amount_paid', 'date_paid', 'paid_by', 'status']
    list_filter = ['status']
    search_fields = ['bill__name']
