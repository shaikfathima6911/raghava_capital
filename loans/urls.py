from django.urls import path
from . import views

urlpatterns = [
    path("add/", views.add_loan, name="add_loan"),
    path("list/", views.loan_list, name="loan_list"),
]