from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Household, Member
from finance.models import Category


DEFAULT_CATEGORIES = [
    # Expense categories
    ('Groceries', 'expense'),
    ('Rent', 'expense'),
    ('Transport', 'expense'),
    ('School Fees', 'expense'),
    ('Medical', 'expense'),
    ('Electricity', 'expense'),
    ('Water', 'expense'),
    ('Entertainment', 'expense'),
    ('Clothing', 'expense'),
    ('Other Expense', 'expense'),
    # Income categories
    ('Salary', 'income'),
    ('Freelance', 'income'),
    ('Business', 'income'),
    ('Other Income', 'income'),
]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    household_name = forms.CharField(
        max_length=100,
        help_text='Enter your family name e.g. The Mokoena Family'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'household_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            household = Household.objects.create(
                name=self.cleaned_data['household_name']
            )
            Member.objects.create(
                user=user,
                household=household,
                role='admin'
            )
            # Create default categories
            for name, cat_type in DEFAULT_CATEGORIES:
                Category.objects.create(
                    name=name,
                    category_type=cat_type,
                    household=household
                )
        return user