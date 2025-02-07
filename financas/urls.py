from django.urls import path, URLPattern

from financas.views.views import FinancasCreateNotionView, FinancasDeleteNotionView, FinancasFindByIdView, FinancasCreateView, FinancasDeleteView, FinancasFindyByIdNotionView, FinancasFindyByNotionIdView, FinancasListNotionView, FinancasListView, FinancasUpdateNotionView, FinancasUpdateView

notion_urls: list[URLPattern] = [
    path('financas/create/notion/', FinancasCreateNotionView.as_view(), name='Criar  Finanças no Notion'),
    path('financas/list/notion/', FinancasListNotionView.as_view(), name='Listar todas as Finanças do Notion'),
    path('financas/findbynotion/<str:notion_page_id>/', FinancasFindyByIdNotionView.as_view(),  name='Buscar Dados pelo ID do Notion'),
    path('financas/update/notion/<str:notion_page_id>', FinancasUpdateNotionView.as_view(), name='Atualizar Dados no Notion'),
    path('financas/delete/notion/<str:notion_page_id>',FinancasDeleteNotionView.as_view(), name='Deletar Dados do Notion')
]

urlpatterns = [
    path('financas/create/', FinancasCreateView.as_view(), name='Criar  Finanças'),
    path('financas/list', FinancasListView.as_view(), name='Listas todas as Finanças'),
    path('financas/findid/<str:notion_page_id>/', FinancasFindyByNotionIdView.as_view(),  name='Buscar Dados pelo ID do Notion'),
    path('financas/findby/<uuid:pk>', FinancasFindByIdView.as_view(),  name='Buscar dados pelo ID'),
    path('financas/update/<uuid:pk>', FinancasUpdateView.as_view(), name='Atualizar Dados'),
    path('financas/delete/<uuid:pk>',FinancasDeleteView.as_view(), name='Deletar Dados'),
] + notion_urls
