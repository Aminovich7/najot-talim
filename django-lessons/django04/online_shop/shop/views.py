from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm, CategoryForm, SearchForm


# ─── PRODUCT VIEWS ────────────────────────────────────────────────────────────

def product_list(request):
    """Barcha mahsulotlar ro'yxati + qidiruv + kategoriya filtri"""
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()
    search_form = SearchForm(request.GET)

    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    context = {
        'products': products,
        'categories': categories,
        'search_form': search_form,
        'query': query,
        'selected_category': category_id,
        'total_count': products.count(),
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, pk):
    """Mahsulot tafsilotlari"""
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(
        category=product.category
    ).exclude(pk=pk)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related': related,
    })


def product_create(request):
    """Yangi mahsulot qo'shish"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"✅ '{product.name}' muvaffaqiyatli qo'shildi!")
            return redirect('shop:product_detail', pk=product.pk)
        else:
            messages.error(request, "❌ Formada xatoliklar mavjud. Iltimos tekshirib ko'ring.")
    else:
        form = ProductForm()

    return render(request, 'shop/product_form.html', {
        'form': form,
        'title': "Yangi mahsulot qo'shish",
        'btn_label': "Qo'shish",
        'action': 'create',
    })


def product_update(request, pk):
    """Mahsulotni tahrirlash"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"✅ '{product.name}' muvaffaqiyatli yangilandi!")
            return redirect('shop:product_detail', pk=product.pk)
        else:
            messages.error(request, "❌ Formada xatoliklar mavjud.")
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/product_form.html', {
        'form': form,
        'product': product,
        'title': f"Tahrirlash: {product.name}",
        'btn_label': "Saqlash",
        'action': 'update',
    })


def product_delete(request, pk):
    """Mahsulotni o'chirish"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"🗑️ '{name}' o'chirildi.")
        return redirect('shop:product_list')

    return render(request, 'shop/product_confirm_delete.html', {
        'product': product,
    })


# ─── CATEGORY VIEWS ───────────────────────────────────────────────────────────

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"✅ '{cat.name}' kategoriyasi qo'shildi!")
            return redirect('shop:category_list')
    else:
        form = CategoryForm()
    return render(request, 'shop/category_form.html', {
        'form': form,
        'title': "Yangi kategoriya",
        'btn_label': "Qo'shish",
    })


def category_update(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, f"✅ '{cat.name}' yangilandi!")
            return redirect('shop:category_list')
    else:
        form = CategoryForm(instance=cat)
    return render(request, 'shop/category_form.html', {
        'form': form,
        'title': f"Tahrirlash: {cat.name}",
        'btn_label': "Saqlash",
    })


def category_delete(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        name = cat.name
        cat.delete()
        messages.success(request, f"🗑️ '{name}' kategoriyasi o'chirildi.")
        return redirect('shop:category_list')
    return render(request, 'shop/category_confirm_delete.html', {'category': cat})
