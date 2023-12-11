# myapp/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    CountryListView,
    CountryCreateView,
    CountryUpdateView,
    CountryDeleteView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    CountryListCreateAPIView,
    CountryDetailAPIView,
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    DestinationCitySearch,
    CalculateFreightView,
)
from django.contrib.auth.views import LoginView, LogoutView

app_name = "cargo_app"

urlpatterns = [
    # Template URLs
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("countries/", CountryListView.as_view(), name="country-list"),
    path("countries/create/", CountryCreateView.as_view(), name="country-create"),
    path(
        "countries/<int:pk>/update/", CountryUpdateView.as_view(), name="country-update"
    ),
    path(
        "countries/<int:pk>/delete/", CountryDeleteView.as_view(), name="country-delete"
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path(
        "categories/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    # REST API URLs
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "api/countries/",
        CountryListCreateAPIView.as_view(),
        name="api-country-list-create",
    ),
    path(
        "api/countries/<int:pk>/",
        CountryDetailAPIView.as_view(),
        name="api-country-detail",
    ),
    path(
        "api/categories/",
        CategoryListCreateAPIView.as_view(),
        name="api-category-list-create",
    ),
    path(
        "api/categories/<int:pk>/",
        CategoryDetailAPIView.as_view(),
        name="api-category-detail",
    ),
    path(
        "api/destination/",
        DestinationCitySearch.as_view(),
        name="api-destination-search",
    ),
    path(
        "api/calculate/", CalculateFreightView.as_view(), name="api-calculate-freight"
    ),
]
