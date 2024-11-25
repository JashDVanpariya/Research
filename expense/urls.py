
from django.urls import path

from . import views

urlpatterns = [

    path('', views.expenses_list, name='expenses-list'),

    path('create/', views.create_expense, name='create-expense'),

    path('edit/<expense_id>/', views.edit_expense, name='edit-expense'),

    path('delete/<expense_id>/', views.delete_expense, name='delete-expense')

]