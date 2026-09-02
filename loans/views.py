from django.shortcuts import render, redirect
from django.db.models import Sum

from .forms import LoanForm
from .models import Loan


def add_loan(request):
    if request.method == "POST":
        form = LoanForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("loan_list")
    else:
        form = LoanForm()

    return render(
        request,
        "loans/add_loan.html",
        {"form": form}
    )


def loan_list(request):
    loans = Loan.objects.all()

    for loan in loans:
        paid_amount = loan.payments.aggregate(
            total=Sum("amount")
        )["total"] or 0

        loan.paid_amount = paid_amount
        loan.remaining_amount = loan.total_amount - paid_amount

    return render(
        request,
        "loans/loan_list.html",
        {"loans": loans}
    )