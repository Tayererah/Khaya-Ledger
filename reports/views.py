from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from finance.models import Expense, Income, Category
from django.db.models import Sum
from datetime import date
import json


@login_required
def reports_view(request):
    household = request.user.member.household
    today = date.today()

    # --- Monthly Expenses by Category (Pie Chart) ---
    expense_by_category = Expense.objects.filter(
        household=household,
        date__month=today.month,
        date__year=today.year
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')

    pie_labels = [item['category__name'] for item in expense_by_category]
    pie_data   = [float(item['total']) for item in expense_by_category]

    # --- Last 6 Months Income vs Expenses (Bar Chart) ---
    months_labels = []
    income_data   = []
    expense_data  = []

    for i in range(5, -1, -1):
        month = today.month - i
        year  = today.year
        if month <= 0:
            month += 12
            year  -= 1

        label = date(year, month, 1).strftime('%b %Y')
        months_labels.append(label)

        month_income = Income.objects.filter(
            household=household,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        month_expense = Expense.objects.filter(
            household=household,
            date__month=month,
            date__year=year
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        income_data.append(float(month_income))
        expense_data.append(float(month_expense))

    # --- Top 5 Expenses This Month ---
    top_expenses = Expense.objects.filter(
        household=household,
        date__month=today.month,
        date__year=today.year
    ).order_by('-amount')[:5]

    # --- Monthly Totals ---
    total_income = Income.objects.filter(
        household=household,
        date__month=today.month,
        date__year=today.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expenses = Expense.objects.filter(
        household=household,
        date__month=today.month,
        date__year=today.year
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'today': today,
        'pie_labels':    json.dumps(pie_labels),
        'pie_data':      json.dumps(pie_data),
        'months_labels': json.dumps(months_labels),
        'income_data':   json.dumps(income_data),
        'expense_data':  json.dumps(expense_data),
        'top_expenses':  top_expenses,
        'total_income':  total_income,
        'total_expenses': total_expenses,
        'balance':       total_income - total_expenses,
        'expense_by_category': expense_by_category,
    }
    return render(request, 'reports/reports.html', context)