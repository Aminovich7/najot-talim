from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Phone
from django.db.models import Q


class PhoneListView(ListView):
    model = Phone
    template_name = 'phone_list.html'
    context_object_name = 'phones'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Phone.objects.filter(
                Q(brand__icontains=query) |
                Q(model__icontains=query)
            )

        return Phone.objects.all()


class PhoneCreateView(CreateView):
    model = Phone
    fields = ['brand', 'model', 'price', 'storage', 'color']
    template_name = 'phone_form.html'
    success_url = reverse_lazy('phone-list')


class PhoneUpdateView(UpdateView):
    model = Phone
    fields = ['brand', 'model', 'price', 'storage', 'color']
    template_name = 'phone_form.html'
    success_url = reverse_lazy('phone-list')


class PhoneDeleteView(DeleteView):
    model = Phone
    template_name = 'phone_confirm_delete.html'
    success_url = reverse_lazy('phone-list')