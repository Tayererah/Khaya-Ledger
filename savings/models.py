from django.db import models
from datetime import date
from accounts.models import Household


class SavingsGoal(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField()
    is_achieved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100

    def monthly_needed(self):
        months_left = (
            (self.target_date.year - date.today().year) * 12 +
            (self.target_date.month - date.today().month)
        )
        remaining = self.target_amount - self.current_amount
        return remaining / months_left if months_left > 0 else remaining

    def __str__(self):
        return f"{self.name} - {self.progress_percentage():.1f}%"