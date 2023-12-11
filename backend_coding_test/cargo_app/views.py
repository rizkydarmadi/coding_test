# myapp/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework import generics
from .models import Country, Category
from .serializers import (
    CountrySerializer,
    CategorySerializer,
    CalculateFreightSerializer,
)
from .forms import CountryForm, CategoryForm
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


# Template Views
class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = "country_list.html"
    context_object_name = "countries"


class CountryCreateView(LoginRequiredMixin, CreateView):
    model = Country
    template_name = "country_form.html"
    form_class = CountryForm
    success_url = reverse_lazy("cargo_app:country-list")


class CountryUpdateView(LoginRequiredMixin, UpdateView):
    model = Country
    template_name = "country_form.html"
    form_class = CountryForm
    success_url = reverse_lazy("cargo_app:country-list")


class CountryDeleteView(LoginRequiredMixin, DeleteView):
    model = Country
    template_name = "country_confirm_delete.html"
    success_url = reverse_lazy("cargo_app:country-list")


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy("cargo_app:category-list")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = "category_form.html"
    form_class = CategoryForm
    success_url = reverse_lazy("cargo_app:category-list")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "category_confirm_delete.html"
    success_url = reverse_lazy("cargo_app:category-list")


# REST API Views
class CountryListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]  # Optional
    permission_classes = [IsAuthenticated]  # Optional
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["country_name"]


class CountryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]  # Optional
    permission_classes = [IsAuthenticated]  # Optional
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]  # Optional
    permission_classes = [IsAuthenticated]  # Optional
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["category_title"]

    def get_queryset(self):
        country_id = self.request.query_params.get("country_id")
        if country_id:
            return Category.objects.filter(country_id=country_id)
        return Category.objects.all()


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]  # Optional
    permission_classes = [IsAuthenticated]  # Optional
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DestinationCitySearch(APIView):
    authentication_classes = [JWTAuthentication]  # Optional
    permission_classes = [IsAuthenticated]  # Optional

    def get(self, request, *args, **kwargs):
        search_query = request.query_params.get("search")

        if not search_query:
            return Response(
                {"error": "Search query parameter 'search' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # RajaOngkir API endpoint for searching cities
        api_url = "https://api.rajaongkir.com/starter/city"
        api_key = "1d844e5a8289abd6a8b9572281eae539"  # Replace with your actual API key

        headers = {
            "key": api_key,
        }
        try:
            response = requests.get(api_url, headers=headers)
            data = response.json()

            # Extract relevant information from the RajaOngkir API response
            results = data.get("rajaongkir", {}).get("results", [])

            matching_cities = []

            for city in results:
                if search_query.lower() in city["city_name"].lower():
                    matching_cities.append(city)

            # Return the extracted information
            return Response(matching_cities, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error in connecting to the RajaOngkir API: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CalculateFreightView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CalculateFreightSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        country_id = serializer.validated_data["country_id"]
        category_id = serializer.validated_data["category_id"]
        destination_id = serializer.validated_data["destination_id"]
        weight = serializer.validated_data["weight"]

        url_rj_ongkr = "https://api.rajaongkir.com/starter/cost"

        payload = {
            "origin": 152,
            "destination": destination_id,
            "weight": weight,
            "courier": "jne",
        }

        headers = {
            "Content-Type": "application/json",
            "key": "1d844e5a8289abd6a8b9572281eae539",
        }

        try:
            response = requests.request(
                "POST", url_rj_ongkr, json=payload, headers=headers
            )

            data = response.json()

            average_cost = [i["costs"] for i in data["rajaongkir"]["results"]]

            all_value = [i["cost"][0]["value"] for i in average_cost[0]]

            average_domestic = sum(all_value) / len(all_value)

            country = Country.objects.get(pk=country_id)
            category = Category.objects.get(pk=category_id)

            international_price = weight * category.price_per_kilo
            domestic_price = average_domestic

            total_price = float(international_price) + float(domestic_price)

            response_data = {
                "origin": country.country_name,
                "destination": data["rajaongkir"]["destination_details"]["city_name"],
                "category_name": category.category_title,
                "international_price": international_price,
                "domestic_price": domestic_price,
                "total_price": total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Country.DoesNotExist:
            return Response(
                {"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except requests.exceptions.RequestException:
            return Response(
                {"error": "Destination not found"}, status=status.HTTP_404_NOT_FOUND
            )
