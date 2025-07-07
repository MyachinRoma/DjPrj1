from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ProductForm, ProductModeratorForm
from .models import Product, Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import get_product_from_cache


@login_required
def my_view(request):
    return render(request, 'catalog/home.html')

class ProductService:
    @staticmethod
    def get_products_by_category(category_id):
        return Product.objects.filter(category_id=category_id)

class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return get_product_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category_id')
        if category_id:
            context['products'] = ProductService.get_products_by_category(category_id)
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner():
            self.object.views_counter += 1
            self.object.save()
            return self.object
        raise PermissionDenied

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product")


    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("pk")])


    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perms("catalog.can_edit_name") and user.has_perms("catalog.can_edit_description"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product")


class UnpublishProductView(LoginRequiredMixin, View):

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden("У вас недостаточно прав для снятия продукта с публикации")

        product.is_published = False
        product.save()

        return redirect('catalog:product', pk=product.id)
