from django.urls import path

from financas.views.views import FinancasFindByIdView, FinancasCreateView, FinancasDeleteView, FinancasFindyByNotionIdView, FinancasListView, FinancasUpdateView

urlpatterns = [
    path('financas/create/',  FinancasCreateView.as_view(), name='create'),
    path('financas/list',   FinancasListView.as_view(), name='list'),
    path('financas/findby/<uuid:pk>',
         FinancasFindByIdView.as_view(),  name='findby_id'),
    path('financas/findid/<str:notion_page_id>/',
         FinancasFindyByNotionIdView.as_view(),  name='findby_notion_id'),
    path('financas/update/<uuid:pk>',
         FinancasUpdateView.as_view(), name='update'),
    path('financas/delete/<uuid:pk>',
         FinancasDeleteView.as_view(), name='delete')

]
