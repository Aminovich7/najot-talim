from django.shortcuts import render
from .models import Category, Services
from django.shortcuts import redirect, get_object_or_404



def list_category(request):
    category = Category.objects.all()
    return render(request, 'list_category.html', context={'category': category})

def create_category(request):
    if request.method == 'POST':
        name = request.post.get('name')
        desc = request.post.get('desc')

        category = Category(name = name, desc = desc)
        category.save()

    return render(request, 'create_category.html')


def update_category(request, id):
    category = Category.objects.filter(id=id)
    if request.method == 'POST':
        category.name = request.post.get('name')
        category.desc = request.post.get('desc')

        category = Category(name = category.name, desc = category.desc)
        category.save()

    return render(request, 'list_category.html')

def delete_category(request, id):
    category = Category.objects.filter(id=id)
    if request.method == 'POST':
        if category:
            category.delete()

            return redirect('list-category')

    return render(request, 'delete_category.html', context={'category': category})


def list_services(request):
    service = Category.objects.all()
    return render(request, 'list_service.html', context={'service': service})



def create_service(request):
    if request.method == 'POST':
        title = request.post.get('title')
        description = request.post.get('description')
        price = request.post.get('price')
        category = request.post.get('category')
        service = Category(title = title, description = description, price = price, category = category)
        service.save()

    return render(request, 'create_service.html')


def delete_service(request, id):
    service = Services.objects.filter(id=id)
    if request.method == 'POST':
        if service:
            service.delete()

            return redirect('service-list')

    return render(request, 'delete_service.html', context={'service': service})



def update_service(request, id):
    service = Services.objects.filter(id=id)
    if request.method == 'POST':
        service.title = request.post.get('name')
        service.description = request.post.get('desc')
        ## davomi bor
        service = Category(name = service.title, desc = category.desc)
        service.save()

    return render(request, 'list_category.html')