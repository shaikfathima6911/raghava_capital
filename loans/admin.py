from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "loan_amount",
        "interest_amount",
        "total_amount",
        "weekly_payment",
        "start_date",
        "status",
    )

    list_filter = ("status", "start_date")
    search_fields = ("customer__name",)