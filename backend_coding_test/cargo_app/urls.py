# your_app_name/urls.py
from django.urls import path
from .views import (
    CountryListCreateView,
    CountryDetailView,
    CategoryListCreateView,
    CategoryDetailView,
)

app_name = "cargo_app"


urlpatterns = [
    path("countries/", CountryListCreateView.as_view(), name="country-list"),
    path("countries/<int:pk>/", CountryDetailView.as_view(), name="country-detail"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    # Add other URLs as needed
]
