from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Expense, Income, Category
from .forms import ExpenseForm, IncomeForm
from bills.models import Bill
from savings.models import SavingsGoal
from django.db.models import Sum
from datetime import date

def home_view(request):
    return render(request, 'finance/home.html')


@login_required
def dashboard_view(request):
    today = date.today()
    household = request.user.member.household
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
    recent_expenses = Expense.objects.filter(
        household=household
    ).order_by('-date')[:5]
    upcoming_bills = Bill.objects.filter(
        household=household,
        is_active=True
    ).order_by('due_day')
    savings_goals = SavingsGoal.objects.filter(
        household=household,
        is_achieved=False
    )
    context = {
        'today': today,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': total_income - total_expenses,
        'recent_expenses': recent_expenses,
        'upcoming_bills': upcoming_bills,
        'savings_goals': savings_goals,
    }
    return render(request, 'finance/dashboard.html', context)


@login_required
def expense_list_view(request):
    household = request.user.member.household
    expenses = Expense.objects.filter(
        household=household
    ).order_by('-date')

    # Search & Filter
    search    = request.GET.get('search', '')
    category  = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to   = request.GET.get('date_to', '')

    if search:
        expenses = expenses.filter(description__icontains=search)
    if category:
        expenses = expenses.filter(category__id=category)
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
    if date_to:
        expenses = expenses.filter(date__lte=date_to)

    categories = Category.objects.filter(
        household=household,
        category_type='expense'
    )

    return render(request, 'finance/expense_list.html', {
        'expenses':   expenses,
        'categories': categories,
        'search':     search,
        'category':   category,
        'date_from':  date_from,
        'date_to':    date_to,
    })

@login_required
def expense_add_view(request):
    household = request.user.member.household
    form = ExpenseForm()
    form.fields['category'].queryset = Category.objects.filter(
        household=household,
        category_type='expense'
    )
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.household = household
            expense.member = request.user.member
            expense.save()
            return redirect('finance:expense_list')
    return render(request, 'finance/expense_add.html', {'form': form})


@login_required
def expense_edit_view(request, pk):
    household = request.user.member.household
    expense = get_object_or_404(Expense, pk=pk, household=household)
    form = ExpenseForm(instance=expense)
    form.fields['category'].queryset = Category.objects.filter(
        household=household,
        category_type='expense'
    )
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('finance:expense_list')
    return render(request, 'finance/expense_add.html', {
        'form': form,
        'edit': True
    })


@login_required
def expense_delete_view(request, pk):
    household = request.user.member.household
    expense = get_object_or_404(Expense, pk=pk, household=household)
    if request.method == 'POST':
        expense.delete()
        return redirect('finance:expense_list')
    return render(request, 'finance/confirm_delete.html', {
        'item': expense,
        'cancel_url': '/expenses/'
    })


@login_required
def income_list_view(request):
    household = request.user.member.household
    incomes = Income.objects.filter(
        household=household
    ).order_by('-date')
    return render(request, 'finance/income_list.html', {'incomes': incomes})


@login_required
def income_add_view(request):
    household = request.user.member.household
    form = IncomeForm()
    form.fields['category'].queryset = Category.objects.filter(
        household=household,
        category_type='income'
    )
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.household = household
            income.member = request.user.member
            income.save()
            return redirect('finance:income_list')
    return render(request, 'finance/income_add.html', {'form': form})


@login_required
def income_edit_view(request, pk):
    household = request.user.member.household
    income = get_object_or_404(Income, pk=pk, household=household)
    form = IncomeForm(instance=income)
    form.fields['category'].queryset = Category.objects.filter(
        household=household,
        category_type='income'
    )
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('finance:income_list')
    return render(request, 'finance/income_add.html', {
        'form': form,
        'edit': True
    })


@login_required
def income_delete_view(request, pk):
    household = request.user.member.household
    income = get_object_or_404(Income, pk=pk, household=household)
    if request.method == 'POST':
        income.delete()
        return redirect('finance:income_list')
    return render(request, 'finance/confirm_delete.html', {
        'item': income,
        'cancel_url': '/income/'
    })