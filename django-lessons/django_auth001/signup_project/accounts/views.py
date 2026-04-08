from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import CustomUserCreationForm

Foydalanuvchi = get_user_model()


class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        admins = Foydalanuvchi.objects.all()
        return render(request, 'registration/signup.html', context={
            'form': form,
            'admins': admins,
        })

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        admins = Foydalanuvchi.objects.all()
        if form.is_valid():
            form.save()
            return redirect('signup')

        return render(request, 'registration/signup.html', {
            "form": form,
            "admins": admins,
        })


