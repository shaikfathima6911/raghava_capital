from django.db import models
from customers.models import Customer
from loans.models import Loan


class Payment(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateField(
        auto_now_add=True
    )

    payment_method = models.CharField(
        max_length=50,
        default="Cash"
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.customer.name} - ₹{self.amount}"
