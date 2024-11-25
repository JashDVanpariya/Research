import os
from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
#from demoproj.pythonlibrary.pythonlibrary.expense import calculate_total_expenses
from expensetrackerlib import tracker




def expenses_list(request):
    expenses = Expense.objects.all()
    total_amount =tracker.calculate_total_expenses(expenses)
    context = {
        'expenses': expenses,
        'total_amount': total_amount,
    }
    return render(request, 'expense/list.html', context)

def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses-list')
    else:
        form = ExpenseForm()
    
    context = {
        'form': form,
    }
    return render(request, 'expense/create.html', context)

def edit_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses-list')
    else:
        form = ExpenseForm(instance=expense)
    
    context = {
        'expense': expense,
        'form': form,
    }
    return render(request, 'expense/edit.html', context)

def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses-list')
    
    context = {
        'expense': expense,
    }
    return render(request, 'expense/delete.html', context)
