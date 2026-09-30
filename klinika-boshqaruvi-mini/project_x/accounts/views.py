from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UpdateProfileForm


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Foydalanuvchi nomi yoki parol noto\'g\'ri!')
        return super().form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Hisob muvaffaqiyatli yaratildi! Iltimos, kiring.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Xatolik yuz berdi. Iltimos, qayta urinib ko\'ring.')
        return super().form_invalid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profil muvaffaqiyatli yangilandi!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Xatolik yuz berdi. Iltimos, qayta urinib ko\'ring.')
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz!')
    return redirect('login')