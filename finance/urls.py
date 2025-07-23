
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('income/', views.income_list, name='income_list'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-category/', views.add_category, name='add_category'),
    path('api/chart-data/', views.chart_data, name='chart_data'),
    path('set-monthly-budget/', views.set_monthly_budget, name='set_monthly_budget'),
]
