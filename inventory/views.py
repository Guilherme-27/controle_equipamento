from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Ambiente, Equipamento, Status


class AmbienteForm(forms.ModelForm):
    class Meta:
        model = Ambiente
        fields = ["nome", "descricao"]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ["nome", "ambiente", "status"]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ambiente': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class EquipamentoListView(LoginRequiredMixin, ListView):
    model = Equipamento
    template_name = "inventory/equipamento_list.html"
    context_object_name = "equipamentos"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Busca por nome
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(nome__icontains=q)
        # Filtro por ambiente
        ambiente_id = self.request.GET.get('ambiente')
        if ambiente_id:
            queryset = queryset.filter(ambiente_id=ambiente_id)
        # Filtro por status
        status_id = self.request.GET.get('status')
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        # Ordenação existente
        self.order = self.request.GET.get('order', 'nome')
        if self.order == 'ambiente':
            queryset = queryset.order_by('ambiente__nome')
        elif self.order == '-ambiente':
            queryset = queryset.order_by('-ambiente__nome')
        elif self.order == 'status':
            queryset = queryset.order_by('status__nome')
        elif self.order == '-status':
            queryset = queryset.order_by('-status__nome')
        else:
            queryset = queryset.order_by('nome')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_order'] = self.order
        # Filtros atuais
        context['current_q'] = self.request.GET.get('q', '')
        context['current_ambiente'] = self.request.GET.get('ambiente', '')
        context['current_status'] = self.request.GET.get('status', '')
        # Dados para dropdowns de filtro
        context['ambientes'] = Ambiente.objects.all()
        context['statuses'] = Status.objects.all()
        return context


class EquipamentoCreateView(LoginRequiredMixin, CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "inventory/equipamento_form.html"

    def get_success_url(self):
        ambiente_id = self.request.GET.get('ambiente') or self.object.ambiente.pk
        if ambiente_id:
            return reverse_lazy("ambiente_detail", kwargs={"pk": ambiente_id})
        return reverse_lazy("equipamento_list")

    def get_initial(self):
        initial = super().get_initial()
        ambiente_id = self.request.GET.get('ambiente')
        if ambiente_id:
            try:
                initial['ambiente'] = Ambiente.objects.get(pk=ambiente_id)
            except Ambiente.DoesNotExist:
                pass
        return initial


class EquipamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "inventory/equipamento_form.html"

    def get_success_url(self):
        ambiente_id = self.object.ambiente.pk
        return reverse_lazy("ambiente_detail", kwargs={"pk": ambiente_id})


class EquipamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipamento
    template_name = "inventory/equipamento_confirm_delete.html"

    def get_success_url(self):
        ambiente_id = self.object.ambiente.pk
        return reverse_lazy("ambiente_detail", kwargs={"pk": ambiente_id})


class AmbienteListView(LoginRequiredMixin, ListView):
    model = Ambiente
    template_name = "inventory/ambiente_list.html"
    context_object_name = "ambientes"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ambientes = context['ambientes']
        ambientes_with_counts = []
        for ambiente in ambientes:
            counts = Equipamento.objects.filter(ambiente=ambiente).values('status__nome').annotate(count=Count('status')).order_by('status__nome')
            count_dict = {}
            for item in counts:
                nome = item['status__nome']
                if 'Operante' in nome:
                    count_dict['operante'] = item['count']
                elif 'Atenção' in nome:
                    count_dict['parcial'] = item['count']
                elif 'Inoperante' in nome:
                    count_dict['inoperante'] = item['count']
            ambientes_with_counts.append({'ambiente': ambiente, 'counts': count_dict})
        context['ambientes_with_counts'] = ambientes_with_counts
        return context


class AmbienteDetailView(LoginRequiredMixin, DetailView):
    model = Ambiente
    template_name = "inventory/ambiente_detail.html"
    context_object_name = "ambiente"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipamentos = Equipamento.objects.filter(ambiente=self.object)
        paginator = Paginator(equipamentos, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['equipamentos'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = paginator.num_pages > 1
        return context


class AmbienteCreateView(LoginRequiredMixin, CreateView):
    model = Ambiente
    form_class = AmbienteForm
    template_name = "inventory/ambiente_form.html"
    success_url = reverse_lazy("ambiente_list")


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "inventory/status_list.html"
    context_object_name = "statuses"


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ["nome", "descricao"]
    template_name = "inventory/status_form.html"
    success_url = reverse_lazy("status_list")


class AmbienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Ambiente
    form_class = AmbienteForm
    template_name = "inventory/ambiente_form.html"
    success_url = reverse_lazy("ambiente_list")


class AmbienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Ambiente
    template_name = "inventory/ambiente_confirm_delete.html"
    success_url = reverse_lazy("ambiente_list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.has_linked_equipamentos:
            return render(request, 'inventory/cannot_delete.html', {
                'message': 'Não é possível excluir o ambiente pois existem equipamentos vinculados a este.',
                'cancel_url': reverse_lazy('ambiente_list')
            })
        return super().get(request, *args, **kwargs)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ["nome", "descricao"]
    template_name = "inventory/status_form.html"
    success_url = reverse_lazy("status_list")


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "inventory/status_confirm_delete.html"
    success_url = reverse_lazy("status_list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.has_linked_equipamentos:
            return render(request, 'inventory/cannot_delete.html', {
                'message': 'Não é possível excluir o status pois existem equipamentos vinculados a este.',
                'cancel_url': reverse_lazy('status_list')
            })
        return super().get(request, *args, **kwargs)
