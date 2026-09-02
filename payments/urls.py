from django.urls import path

from . import views


urlpatterns = [

    path(
        "add/",
        views.add_payment,
        name="add_payment"
    ),

    path(
        "list/",
        views.payment_list,
        name="payment_list"
    ),

    path(
        "reports/",
        views.reports,
        name="reports"
    ),

]

