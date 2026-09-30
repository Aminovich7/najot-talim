from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Doctor, Consultation, Surgery, Room
from .forms import DoctorForm, ConsultationForm, SurgeryForm, RoomForm
#report uchun ishlatilgan
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce # null valueni 0 deb olib hisoblash uchun ishlatiladi
from decimal import Decimal
from django.utils.dateparse import parse_date
from collections import defaultdict




# ==================== DOCTOR VIEWS ====================

class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    template_name = 'doctors/doctor_list.html'
    context_object_name = 'doctors'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            ) | queryset.filter(
                specialty__icontains=search
            )
        return queryset


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/doctor_form.html'
    success_url = reverse_lazy('doctor-list')

    def form_valid(self, form):
        messages.success(self.request, 'Shifokor muvaffaqiyatli qo\'shildi!')
        return super().form_valid(form)


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'doctors/doctor_form.html'
    success_url = reverse_lazy('doctor-list')

    def form_valid(self, form):
        messages.success(self.request, 'Shifokor ma\'lumotlari yangilandi!')
        return super().form_valid(form)


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = Doctor
    template_name = 'doctors/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Shifokor o\'chirildi!')
        return super().delete(request, *args, **kwargs)


# ==================== CONSULTATION VIEWS ====================

class ConsultationListView(LoginRequiredMixin, ListView):
    model = Consultation
    template_name = 'consultations/consultation_list.html'
    context_object_name = 'consultations'
    paginate_by = 20
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.GET.get('doctor')
        consultation_type = self.request.GET.get('type')

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        if consultation_type:
            queryset = queryset.filter(type=consultation_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        return context


class ConsultationCreateView(LoginRequiredMixin, CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'consultations/consultation_form.html'
    success_url = reverse_lazy('consultation-list')

    def form_valid(self, form):
        messages.success(self.request, 'Konsultatsiya qo\'shildi!')
        return super().form_valid(form)


class ConsultationUpdateView(LoginRequiredMixin, UpdateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'consultations/consultation_form.html'
    success_url = reverse_lazy('consultation-list')

    def form_valid(self, form):
        messages.success(self.request, 'Konsultatsiya yangilandi!')
        return super().form_valid(form)


class ConsultationDeleteView(LoginRequiredMixin, DeleteView):
    model = Consultation
    template_name = 'consultations/consultation_confirm_delete.html'
    success_url = reverse_lazy('consultation-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Konsultatsiya o\'chirildi!')
        return super().delete(request, *args, **kwargs)


# ==================== SURGERY VIEWS ====================

class SurgeryListView(LoginRequiredMixin, ListView):
    model = Surgery
    template_name = 'surgeries/surgery_list.html'
    context_object_name = 'surgeries'
    paginate_by = 20
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.GET.get('doctor')

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        return context


class SurgeryCreateView(LoginRequiredMixin, CreateView):
    model = Surgery
    form_class = SurgeryForm
    template_name = 'surgeries/surgery_form.html'
    success_url = reverse_lazy('surgery-list')

    def form_valid(self, form):
        messages.success(self.request, 'Operatsiya qo\'shildi!')
        return super().form_valid(form)


class SurgeryUpdateView(LoginRequiredMixin, UpdateView):
    model = Surgery
    form_class = SurgeryForm
    template_name = 'surgeries/surgery_form.html'
    success_url = reverse_lazy('surgery-list')

    def form_valid(self, form):
        messages.success(self.request, 'Operatsiya yangilandi!')
        return super().form_valid(form)


class SurgeryDeleteView(LoginRequiredMixin, DeleteView):
    model = Surgery
    template_name = 'surgeries/surgery_confirm_delete.html'
    success_url = reverse_lazy('surgery-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Operatsiya o\'chirildi!')
        return super().delete(request, *args, **kwargs)


# ==================== ROOM VIEWS ====================

class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'rooms/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 20
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.GET.get('doctor')

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        return context


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('room-list')

    def form_valid(self, form):
        messages.success(self.request, 'Palata qo\'shildi!')
        return super().form_valid(form)


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('room-list')

    def form_valid(self, form):
        messages.success(self.request, 'Palata yangilandi!')
        return super().form_valid(form)


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'rooms/room_confirm_delete.html'
    success_url = reverse_lazy('room-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Palata o\'chirildi!')
        return super().delete(request, *args, **kwargs)


#REPORTlAR QISMI
class ConsultationReportView(LoginRequiredMixin, TemplateView):
    template_name = 'consultations/consultation_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        consultations = Consultation.objects.all()

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            consultations = consultations.filter(date__date__gte=parse_date(date_from))
        if date_to:
            consultations = consultations.filter(date__date__lte=parse_date(date_to))

        # Income by type
        korik = consultations.filter(type='korik').aggregate(
            total=Coalesce(Sum('amount'), Decimal('0')),
            count=Count('id')
        )
        qayta_korik = consultations.filter(type='qaytakorik').aggregate(
            total=Coalesce(Sum('amount'), Decimal('0')),
            count=Count('id')
        )

        # Doctor share & clinic profit (Python-level, since formula mixes fields)
        total_doctor_share = Decimal('0')
        total_clinic_profit = Decimal('0')
        total_consultation_expense = Decimal('0')
        doctor_shares = defaultdict(lambda: {'name': '', 'total_share': Decimal('0'), 'count': 0})

        for c in consultations:
            minus = c.minus_beshming or Decimal('0')
            doctor_share = (c.amount - minus) * c.doctor_percent / 100
            clinic_profit = c.amount - doctor_share - minus
            total_doctor_share += doctor_share
            total_clinic_profit += clinic_profit
            total_consultation_expense += minus

            if c.doctor_id:
                doctor_shares[c.doctor_id]['name'] = str(c.doctor)
                doctor_shares[c.doctor_id]['total_share'] += doctor_share
                doctor_shares[c.doctor_id]['count'] += 1

        context.update({
            'korik': korik,
            'qayta_korik': qayta_korik,
            'total_income': korik['total'] + qayta_korik['total'],
            'total_doctor_share': round(total_doctor_share),
            'total_clinic_profit': round(total_clinic_profit),
            'total_consultation_expense': total_consultation_expense,
            'doctor_shares': doctor_shares.values(),
        })
        return context


class SurgeryReportView(LoginRequiredMixin, TemplateView):
    template_name = 'surgeries/surgery_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        surgeries = Surgery.objects.all()

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            surgeries = surgeries.filter(date__date__gte=parse_date(date_from))
        if date_to:
            surgeries = surgeries.filter(date__date__lte=parse_date(date_to))

        surgery_total_income = Decimal('0')
        surgery_total_doctor_share = Decimal('0')
        surgery_total_clinic_profit = Decimal('0')
        surgery_total_expense = Decimal('0')
        surgery_doctor_shares = defaultdict(lambda: {'name': '', 'total_share': Decimal('0'), 'count': 0})

        for s in surgeries:
            expense = s.surgery_expense or Decimal('0')
            doctor_share = (s.amount - expense) * s.doctor_percent / 100
            clinic_profit = s.amount - doctor_share - expense
            surgery_total_income += s.amount
            surgery_total_doctor_share += doctor_share
            surgery_total_clinic_profit += clinic_profit
            surgery_total_expense += expense

            if s.doctor_id:
                surgery_doctor_shares[s.doctor_id]['name'] = str(s.doctor)
                surgery_doctor_shares[s.doctor_id]['total_share'] += doctor_share
                surgery_doctor_shares[s.doctor_id]['count'] += 1

        for d in surgery_doctor_shares.values():
            d['total_share'] = int(d['total_share'])

        context.update({
            'surgery_total_income': int(surgery_total_income),
            'surgery_total_doctor_share': int(surgery_total_doctor_share),
            'surgery_total_clinic_profit': int(surgery_total_clinic_profit),
            'surgery_total_expense': int(surgery_total_expense),
            'surgery_doctor_shares': surgery_doctor_shares.values(),
        })
        return context




class RoomReportView(LoginRequiredMixin, TemplateView):
    template_name = 'rooms/room_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        rooms = Room.objects.all()

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            rooms = rooms.filter(date__date__gte=parse_date(date_from))
        if date_to:
            rooms = rooms.filter(date__date__lte=parse_date(date_to))

        room_total_income = Decimal('0')
        room_total_doctor_share = Decimal('0')
        room_total_clinic_profit = Decimal('0')
        room_doctor_shares = defaultdict(lambda: {'name': '', 'total_share': Decimal('0'), 'count': 0})

        for r in rooms:
            doctor_share = r.amount * (r.doctor_percent / 100)
            clinic_profit = r.amount - doctor_share
            room_total_income += r.amount
            room_total_doctor_share += doctor_share
            room_total_clinic_profit += clinic_profit

            if r.doctor_id:
                room_doctor_shares[r.doctor_id]['name'] = str(r.doctor)
                room_doctor_shares[r.doctor_id]['total_share'] += doctor_share
                room_doctor_shares[r.doctor_id]['count'] += 1

        for d in room_doctor_shares.values():
            d['total_share'] = int(d['total_share'])

        context.update({
            'room_total_income': int(room_total_income),
            'room_total_doctor_share': int(room_total_doctor_share),
            'room_total_clinic_profit': int(room_total_clinic_profit),
            'room_doctor_shares': room_doctor_shares.values(),
        })
        return context




class TotalReportView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        consultations = Consultation.objects.all()
        surgeries = Surgery.objects.all()
        rooms = Room.objects.all()

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if date_from:
            consultations = consultations.filter(date__date__gte=parse_date(date_from))
            surgeries = surgeries.filter(date__date__gte=parse_date(date_from))
            rooms = rooms.filter(date__date__gte=parse_date(date_from))
        if date_to:
            consultations = consultations.filter(date__date__lte=parse_date(date_to))
            surgeries = surgeries.filter(date__date__lte=parse_date(date_to))
            rooms = rooms.filter(date__date__lte=parse_date(date_to))

        # --- Consultations ---
        consultation_income = Decimal('0')
        consultation_doctor_share = Decimal('0')
        consultation_expense = Decimal('0')

        for c in consultations:
            minus = c.minus_beshming or Decimal('0')
            doctor_share = (c.amount - minus) * c.doctor_percent / 100
            consultation_income += c.amount
            consultation_doctor_share += doctor_share
            consultation_expense += minus

        consultation_clinic_profit = consultation_income - consultation_doctor_share - consultation_expense

        # --- Surgeries ---
        surgery_income = Decimal('0')
        surgery_doctor_share = Decimal('0')
        surgery_expense = Decimal('0')

        for s in surgeries:
            expense = s.surgery_expense or Decimal('0')
            doctor_share = (s.amount - expense) * s.doctor_percent / 100
            surgery_income += s.amount
            surgery_doctor_share += doctor_share
            surgery_expense += expense

        surgery_clinic_profit = surgery_income - surgery_doctor_share - surgery_expense

        # --- Rooms ---
        room_income = Decimal('0')
        room_doctor_share = Decimal('0')

        for r in rooms:
            doctor_share = r.amount * (r.doctor_percent / 100)
            room_income += r.amount
            room_doctor_share += doctor_share

        room_clinic_profit = room_income - room_doctor_share

        # --- Totals ---
        total_income = consultation_income + surgery_income + room_income
        total_doctor_share = consultation_doctor_share + surgery_doctor_share + room_doctor_share
        total_expense = consultation_expense + surgery_expense
        total_clinic_profit = consultation_clinic_profit + surgery_clinic_profit + room_clinic_profit

        context.update({
            # Consultation
            'consultation_income': int(consultation_income),
            'consultation_doctor_share': int(consultation_doctor_share),
            'consultation_expense': int(consultation_expense),
            'consultation_clinic_profit': int(consultation_clinic_profit),

            # Surgery
            'surgery_income': int(surgery_income),
            'surgery_doctor_share': int(surgery_doctor_share),
            'surgery_expense': int(surgery_expense),
            'surgery_clinic_profit': int(surgery_clinic_profit),

            # Room
            'room_income': int(room_income),
            'room_doctor_share': int(room_doctor_share),
            'room_clinic_profit': int(room_clinic_profit),

            # Totals
            'total_income': int(total_income),
            'total_doctor_share': int(total_doctor_share),
            'total_expense': int(total_expense),
            'total_clinic_profit': int(total_clinic_profit),
        })
        return context