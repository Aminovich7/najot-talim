from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Services


def list_category(request):
    category = Category.objects.all()
    return render(request, 'list_category.html', context={'category': category})


def category_detail(request, id):
    category = get_object_or_404(Category, id=id)         
    return render(request, 'category_detail.html', context={'category': category})


def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')                    
        desc = request.POST.get('desc')
        Category(name=name, desc=desc).save()
    return render(request, 'create_category.html')


def update_category(request, id):
    category = get_object_or_404(Category, id=id)          
    if request.method == 'POST':
        category.name = request.POST.get('name')           
        category.desc = request.POST.get('desc')
        category.save()                                   
        return redirect('category-detail', category.id)
    return render(request, 'update_category.html', context={'category': category})


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('list-category')
    return render(request, 'delete_category.html', context={'category': category})


def list_services(request):
    service = Services.objects.all()                       
    return render(request, 'list_service.html', context={'service': service})


def service_detail(request, id):
    service = get_object_or_404(Services, id=id)
    return render(request, 'service_detail.html', context={'service': service})


def create_service(request):
    if request.method == 'POST':
        title = request.POST.get('title')                 
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        Services(                                          
            title=title,
            description=description,
            price=price,
            category_id=category                         
        ).save()
    return render(request, 'create_service.html')


def delete_service(request, id):
    service = get_object_or_404(Services, id=id)
    if request.method == 'POST':
        service.delete()
        return redirect('service-list')
    return render(request, 'delete_service.html', context={'service': service})


def update_service(request, id):
    service = get_object_or_404(Services, id=id)           
    if request.method == 'POST':
        service.title = request.POST.get('title')         
        service.description = request.POST.get('description')
        service.price = request.POST.get('price')
        service.category_id = request.POST.get('category') 
        service.save()                                     
        return redirect('service-detail', service.id)
    return render(request, 'update-service.html', context={'service': service})




def index(request):
    category = Category.objects.all()
    service = Services.objects.all()
    return render(request, 'index.html', {'category': category, 'service': service})