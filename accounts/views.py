from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from customers.models import Customer
from loans.models import Loan
from payments.models import Payment

from django.db.models import Sum
from django.utils import timezone


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(
        request,
        "accounts/login.html"
    )


def logout_view(request):
    logout(request)
    return redirect("login")


def dashboard(request):

    # -----------------------------
    # Total Customers
    # -----------------------------

    total_customers = Customer.objects.count()


    # -----------------------------
    # Active Loans
    # -----------------------------

    active_loans = Loan.objects.filter(
        status="Active"
    ).count()


    # -----------------------------
    # Total Collection
    # -----------------------------

    total_collection = Payment.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0


    # -----------------------------
    # Today's Collection
    # -----------------------------

    today = timezone.localdate()

    today_collection = Payment.objects.filter(
        payment_date=today
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    # -----------------------------
    # Recent Payments
    # -----------------------------

    recent_payments = Payment.objects.select_related(
        "customer",
        "loan"
    ).order_by(
        "-payment_date",
        "-id"
    )[:5]


    # -----------------------------
    # Last 7 Days Collection
    # -----------------------------

    collection_days = []

    for i in range(6, -1, -1):

        current_date = today - timedelta(days=i)

        amount = Payment.objects.filter(
            payment_date=current_date
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        collection_days.append({
            "date": current_date,
            "label": current_date.strftime("%a"),
            "amount": amount,
        })


    # -----------------------------
    # Find Maximum Collection
    # -----------------------------

    max_collection = max(
        [float(day["amount"]) for day in collection_days],
        default=0
    )


    # -----------------------------
    # Calculate Chart Heights
    # -----------------------------

    for day in collection_days:

        if max_collection > 0:
            day["percentage"] = (
                float(day["amount"]) / max_collection
            ) * 100
        else:
            day["percentage"] = 0


    # -----------------------------
    # Context
    # -----------------------------

    context = {
        "total_customers": total_customers,
        "active_loans": active_loans,
        "total_collection": total_collection,
        "today_collection": today_collection,

        "recent_payments": recent_payments,

        "collection_days": collection_days,

        "today": today,
    }


    return render(
        request,
        "accounts/dashboard.html",
        context
    )

