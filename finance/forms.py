
from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.none(), empty_label="Select a category")
    
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'note', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)
        
        if user and transaction_type:
            self.fields['category'].queryset = Category.objects.filter(
                user=user, 
                category_type=transaction_type
            )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
