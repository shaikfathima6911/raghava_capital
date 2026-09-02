from django.db import models
from customers.models import Customer


class Loan(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Completed", "Completed"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="loans"
    )

    loan_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    interest_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    weekly_payment = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    start_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    def __str__(self):
        return f"{self.customer.name} - {self.loan_amount}"