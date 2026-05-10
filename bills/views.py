from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bill
from .forms import BillForm
from finance.models import Category


@login_required
def bill_list_view(request):
    household = request.user.member.household
    bills = Bill.objects.filter(
        household=household,
        is_active=True
    ).order_by('due_day')
    return render(request, 'bills/bill_list.html', {'bills': bills})


@login_required
def bill_add_view(request):
    household = request.user.member.household
    form = BillForm()
    form.fields['category'].queryset = Category.objects.filter(
        household=household
    )
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.household = household
            bill.save()
            return redirect('bills:bill_list')
    return render(request, 'bills/bill_add.html', {'form': form})


@login_required
def bill_edit_view(request, pk):
    household = request.user.member.household
    bill = get_object_or_404(Bill, pk=pk, household=household)
    form = BillForm(instance=bill)
    form.fields['category'].queryset = Category.objects.filter(
        household=household
    )
    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('bills:bill_list')
    return render(request, 'bills/bill_add.html', {
        'form': form,
        'edit': True
    })


@login_required
def bill_delete_view(request, pk):
    household = request.user.member.household
    bill = get_object_or_404(Bill, pk=pk, household=household)
    if request.method == 'POST':
        bill.delete()
        return redirect('bills:bill_list')
    return render(request, 'finance/confirm_delete.html', {
        'item': bill,
        'cancel_url': '/bills/'
    })