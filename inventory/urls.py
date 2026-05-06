from django.urls import path

from .views import (
    AmbienteCreateView,
    AmbienteDeleteView,
    AmbienteDetailView,
    AmbienteListView,
    AmbienteUpdateView,
    EquipamentoCreateView,
    EquipamentoDeleteView,
    EquipamentoListView,
    EquipamentoUpdateView,
    StatusCreateView,
    StatusListView,
    StatusUpdateView,
    StatusDeleteView,
)

urlpatterns = [
    path("", AmbienteListView.as_view(), name="ambiente_list"),
    path("ambientes/<int:pk>/", AmbienteDetailView.as_view(), name="ambiente_detail"),
    path("equipamentos/", EquipamentoListView.as_view(), name="equipamento_list"),
    path("equipamentos/novo/", EquipamentoCreateView.as_view(), name="equipamento_create"),
    path("equipamentos/<int:pk>/editar/", EquipamentoUpdateView.as_view(), name="equipamento_update"),
    path("equipamentos/<int:pk>/excluir/", EquipamentoDeleteView.as_view(), name="equipamento_delete"),
    path("ambientes/novo/", AmbienteCreateView.as_view(), name="ambiente_create"),
    path("statuses/", StatusListView.as_view(), name="status_list"),
    path("statuses/novo/", StatusCreateView.as_view(), name="status_create"),
    path("ambientes/<int:pk>/editar/", AmbienteUpdateView.as_view(), name="ambiente_update"),
    path("ambientes/<int:pk>/excluir/", AmbienteDeleteView.as_view(), name="ambiente_delete"),
    path("statuses/<int:pk>/editar/", StatusUpdateView.as_view(), name="status_update"),
    path("statuses/<int:pk>/excluir/", StatusDeleteView.as_view(), name="status_delete"),
]
