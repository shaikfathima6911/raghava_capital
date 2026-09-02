from django.shortcuts import render, redirect, get_object_or_404

from .models import Customer
from .forms import CustomerForm


def add_customer(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("customer_list")

    else:
        form = CustomerForm()

    return render(
        request,
        "customers/add_customer.html",
        {"form": form}
    )


def customer_list(request):

    search = request.GET.get("search", "").strip()

    customers = Customer.objects.all().order_by("-id")

    if search:
        customers = customers.filter(
            name__icontains=search
        )

    context = {
        "customers": customers,
        "search": search,
        "total_customers": customers.count(),
    }

    return render(
        request,
        "customers/customer_list.html",
        context
    )


def edit_customer(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():
            form.save()
            return redirect("customer_list")

    else:
        form = CustomerForm(
            instance=customer
        )

    return render(
        request,
        "customers/edit_customer.html",
        {
            "form": form,
            "customer": customer
        }
    )


def delete_customer(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    if request.method == "POST":

        customer.delete()

        return redirect("customer_list")

    return render(
        request,
        "customers/delete_customer.html",
        {
            "customer": customer
        }
    )