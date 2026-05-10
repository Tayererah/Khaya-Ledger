from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Budget
from .forms import BudgetForm
from finance.models import Category
from datetime import date


@login_required
def budget_list_view(request):
    household = request.user.member.household
    today = date.today()
    budgets = Budget.objects.filter(
        household=household
    ).order_by('-year', '-month')

    # Add spent and percentage to each budget
    budget_data = []
    for budget in budgets:
        spent = budget.spent_amount()
        remaining = budget.remaining()
        percentage = budget.percentage_used()
        if percentage > 90:
            status = 'danger'
            status_color = '#e74c3c'
        elif percentage > 70:
            status = 'warning'
            status_color = '#f39c12'
        else:
            status = 'good'
            status_color = '#27ae60'
        budget_data.append({
            'budget': budget,
            'spent': spent,
            'remaining': remaining,
            'percentage': percentage,
            'status_color': status_color,
        })

    return render(request, 'budgets/budget_list.html', {
        'budget_data': budget_data
    })


@login_required
def budget_add_view(request):
    household = request.user.member.household
    form = BudgetForm()
    form.fields['category'].queryset = Category.objects.filter(
        household=household
    )
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.household = household
            budget.save()
            return redirect('budgets:budget_list')
    return render(request, 'budgets/budget_add.html', {'form': form})


@login_required
def budget_edit_view(request, pk):
    household = request.user.member.household
    budget = get_object_or_404(Budget, pk=pk, household=household)
    form = BudgetForm(instance=budget)
    form.fields['category'].queryset = Category.objects.filter(
        household=household
    )
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budgets:budget_list')
    return render(request, 'budgets/budget_add.html', {
        'form': form,
        'edit': True
    })


@login_required
def budget_delete_view(request, pk):
    household = request.user.member.household
    budget = get_object_or_404(Budget, pk=pk, household=household)
    if request.method == 'POST':
        budget.delete()
        return redirect('budgets:budget_list')
    return render(request, 'finance/confirm_delete.html', {
        'item': budget,
        'cancel_url': '/budgets/'
    })