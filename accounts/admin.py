from django.contrib import admin
from .models import Household, Member

@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ['name', 'currency', 'created_at']
    search_fields = ['name']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'household', 'role', 'created_at']
    search_fields = ['user__username']
    list_filter = ['role']
