from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm

def home_view(request):
    products = Product.objects.filter(is_available=True).select_related('owner', 'category')
    categories = Category.objects.all()
    
    q = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    condition = request.GET.get('condition', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if q:
        products = products.filter(Q(name__icontains=q) | Q(brand__icontains=q) | Q(description__icontains=q))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if condition:
        products = products.filter(condition=condition)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'q': q,
        'selected_category': category_slug,
        'selected_condition': condition,
    })

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category, is_available=True).exclude(pk=pk)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related': related})

@login_required
def my_products_view(request):
    products = Product.objects.filter(owner=request.user)
    return render(request, 'store/my_products.html', {'products': products})

@login_required
def product_create_view(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.owner = request.user
        product.save()
        messages.success(request, "Watch listed successfully!")
        return redirect('my_products')
    return render(request, 'store/product_form.html', {'form': form, 'title': 'List a Watch'})

@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Watch updated successfully!")
        return redirect('my_products')
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Edit Watch', 'product': product})

@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Watch removed from listings.")
        return redirect('my_products')
    return render(request, 'store/product_confirm_delete.html', {'product': product})
