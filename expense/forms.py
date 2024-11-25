from django import forms
from django.forms import ModelForm
from .models import Expense

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ('expense_name', 'expense_category', 'description', 'amount', 'date',)

        widgets = {
            'expense_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expense Name'}),
            'expense_category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expense Category'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'Date'}),
        }
