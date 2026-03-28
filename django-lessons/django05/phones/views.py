from django.shortcuts import render
from django.views import View
from .models import Phone
from django.shortcuts import redirect, get_object_or_404

def get_phone_list(request):
    phones = Phone.objects.all()
    return render(request, 'phones.html', context = {'phones': phones})


def add_phone(request):
    if request.method == "POST":
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')

        phone = Phone(brand = brand, model = model, price = price, quantity = quantity)
        phone.save()

        return redirect('list') 
    
    return render(request, 'add_phone.html')



def phone_detail(request, id):
    phone = Phone.objects.filter(id=id).first()
    return render(request, 'phone_detail.html', context={'phone': phone})



def phone_delete(request, id):
    phone = Phone.objects.filter(id=id).first()
    if request.method == "POST":
        if phone:
            phone.delete()
            return redirect('list')
    
    return render(request, 'phone_delete.html', context={'phone': phone})
        
    
    
def update_phone(request, id):
    phone = Phone.objects.filter(id=id).first()

    if request.method == "POST":
        phone = Phone.objects.filter(id=id).first()
        phone.brand = request.POST.get('brand')
        phone.model = request.POST.get('model')
        phone.price = request.POST.get('price')
        phone.quantity = request.POST.get('quantity')
        
        phone.save()
        
        return redirect('detail', phone.id)
        
    
    return render(request, 'update.html', context={'phone': phone})

