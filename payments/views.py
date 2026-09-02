from django.db.models import Sum
from django.shortcuts import render, redirect

from .forms import PaymentForm
from .models import Payment


def add_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("payment_list")
    else:
        form = PaymentForm()

    return render(
        request,
        "payments/add_payment.html",
        {"form": form}
    )


def payment_list(request):
    payments = Payment.objects.all().order_by("-payment_date")

    return render(
        request,
        "payments/payment_list.html",
        {"payments": payments}
    )


def reports(request):

    payments = Payment.objects.all().order_by(
        "-payment_date",
        "-id"
    )

    # -----------------------------
    # SEARCH
    # -----------------------------

    search = request.GET.get("search", "").strip()

    if search:
        payments = payments.filter(
            customer__name__icontains=search
        )


    # -----------------------------
    # PAYMENT METHOD FILTER
    # -----------------------------

    method = request.GET.get("method", "").strip()

    if method:
        payments = payments.filter(
            payment_method__iexact=method
        )


    # -----------------------------
    # DATE FILTER
    # -----------------------------

    payment_date = request.GET.get(
        "payment_date",
        ""
    ).strip()

    if payment_date:
        payments = payments.filter(
            payment_date=payment_date
        )


    # -----------------------------
    # SUMMARY
    # -----------------------------

    total_payments = payments.count()

    total_collection = payments.aggregate(
        total=Sum("amount")
    )["total"] or 0


    cash_collection = payments.filter(
        payment_method__iexact="Cash"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    online_collection = payments.filter(
        payment_method__iexact="Online"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    # -----------------------------
    # OTHER PAYMENT METHODS
    # -----------------------------

    other_collection = payments.exclude(
        payment_method__iexact="Cash"
    ).exclude(
        payment_method__iexact="Online"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0


    context = {

        "payments": payments,

        "total_payments": total_payments,

        "total_collection": total_collection,

        "cash_collection": cash_collection,

        "online_collection": online_collection,

        "other_collection": other_collection,

        "search": search,

        "method": method,

        "payment_date": payment_date,

    }


    return render(
        request,
        "payments/reports.html",
        context
    )
