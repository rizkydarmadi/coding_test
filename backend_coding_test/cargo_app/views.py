# myapp/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework import generics
from .models import Country, Category
from .serializers import CountrySerializer, CategorySerializer
from .forms import CountryForm, CategoryForm
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters

# Template Views
class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'country_list.html'
    context_object_name = 'countries'

class CountryCreateView(LoginRequiredMixin, CreateView):
    model = Country
    template_name = 'country_form.html'
    form_class = CountryForm
    success_url = reverse_lazy('cargo_app:country-list')

class CountryUpdateView(LoginRequiredMixin, UpdateView):
    model = Country
    template_name = 'country_form.html'
    form_class = CountryForm
    success_url = reverse_lazy('cargo_app:country-list')

class CountryDeleteView(LoginRequiredMixin, DeleteView):
    model = Country
    template_name = 'country_confirm_delete.html'
    success_url = reverse_lazy('cargo_app:country-list')

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('cargo_app:category-list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('cargo_app:category-list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('cargo_app:category-list')



# REST API Views
class CountryListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]  # Optional
    permission_classes = [IsAuthenticated]  # Optional
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['country_name']

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
    search_fields = ['category_title']

    def get_queryset(self):
        country_id = self.request.query_params.get('country_id')
        if country_id:
            return Category.objects.filter(country_id=country_id)
        return Category.objects.all()

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]  # Optional
    permission_classes = [IsAuthenticated]  # Optional
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
