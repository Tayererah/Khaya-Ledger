from django import forms
from .models import Bill, BillPayment


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['name', 'amount', 'due_day', 'category']
        widgets = {
            'due_day': forms.NumberInput(attrs={'min': 1, 'max': 31}),
        }


class BillPaymentForm(forms.ModelForm):
    class Meta:
        model = BillPayment
        fields = ['amount_paid', 'date_paid', 'status']
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
        }