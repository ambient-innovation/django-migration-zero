from django.contrib import admin
from django.urls import path

urlpatterns = [
    # django Admin
    path("admin/", admin.site.urls),
]
