from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    address = models.TextField()

    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    weekly_payment = models.DecimalField(max_digits=10, decimal_places=2)

    start_date = models.DateField()

    def __str__(self):
        return self.name