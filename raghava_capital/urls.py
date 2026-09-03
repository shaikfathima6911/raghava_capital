from django.contrib import admin
from django.urls import path, include
from .service_worker import service_worker


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("customers/", include("customers.urls")),
    path("loans/", include("loans.urls")),
    path("payments/", include("payments.urls")),

    path("service-worker.js", service_worker, name="service_worker"),
]