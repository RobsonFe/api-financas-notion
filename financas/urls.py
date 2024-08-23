from django.urls import path

from financas.views.views import FinancasFindByIdView, FinancasCreateView, FinancasDeleteView, FinancasFindyByNotionIdView, FinancasListView, FinancasUpdateView

urlpatterns = [
    path('financas/create/',  FinancasCreateView.as_view(), name='Criar  Finanças'),

    path('financas/list',   FinancasListView.as_view(),
         name='Listas todas as Finanças'),
    path('financas/findby/<uuid:pk>',
         FinancasFindByIdView.as_view(),  name='Buscar dados pelo ID'),
    path('financas/findid/<str:notion_page_id>/',
         FinancasFindyByNotionIdView.as_view(),  name='Buscar Dados pelo ID do Notion'),
    path('financas/update/<uuid:pk>',
         FinancasUpdateView.as_view(), name='Atualizar Dados'),
    path('financas/delete/<uuid:pk>',
         FinancasDeleteView.as_view(), name='Deletar Dados')

]
