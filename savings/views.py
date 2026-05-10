from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SavingsGoal
from .forms import SavingsGoalForm


@login_required
def savings_list_view(request):
    household = request.user.member.household
    goals = SavingsGoal.objects.filter(
        household=household
    ).order_by('target_date')
    return render(request, 'savings/savings_list.html', {'goals': goals})


@login_required
def savings_add_view(request):
    household = request.user.member.household
    form = SavingsGoalForm()
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.household = household
            goal.save()
            return redirect('savings:savings_list')
    return render(request, 'savings/savings_add.html', {'form': form})


@login_required
def savings_edit_view(request, pk):
    household = request.user.member.household
    goal = get_object_or_404(SavingsGoal, pk=pk, household=household)
    form = SavingsGoalForm(instance=goal)
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('savings:savings_list')
    return render(request, 'savings/savings_add.html', {
        'form': form,
        'edit': True
    })


@login_required
def savings_delete_view(request, pk):
    household = request.user.member.household
    goal = get_object_or_404(SavingsGoal, pk=pk, household=household)
    if request.method == 'POST':
        goal.delete()
        return redirect('savings:savings_list')
    return render(request, 'finance/confirm_delete.html', {
        'item': goal,
        'cancel_url': '/savings/'
    })