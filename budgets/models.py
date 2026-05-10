from django.db import models
from django.db.models import Sum
from accounts.models import Household
from finance.models import Category, Expense


class Budget(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def spent_amount(self):
        return Expense.objects.filter(
            household=self.household,
            category=self.category,
            date__month=self.month,
            date__year=self.year
        ).aggregate(total=Sum('amount'))['total'] or 0

    def remaining(self):
        return self.amount - self.spent_amount()

    def percentage_used(self):
        if self.amount == 0:
            return 0
        return (self.spent_amount() / self.amount) * 100

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year}"