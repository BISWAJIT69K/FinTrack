
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm

@login_required
def dashboard(request):
    # Get filter parameters
    filter_type = request.GET.get('filter', 'all')
    
    # Base queryset
    transactions = Transaction.objects.filter(user=request.user)
    
    # Apply filters
    if filter_type == 'daily':
        today = timezone.now().date()
        transactions = transactions.filter(date=today)
    elif filter_type == 'monthly':
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        transactions = transactions.filter(date__gte=start_of_month, date__lte=today)
    
    # Calculate totals
    income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income - expenses
    
    # Recent transactions
    recent_transactions = transactions[:5]
    
    context = {
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'filter_type': filter_type,
    }
    return render(request, 'finance/dashboard.html', context)

@login_required
def income_list(request):
    filter_type = request.GET.get('filter', 'all')
    transactions = Transaction.objects.filter(user=request.user, transaction_type='income')
    
    if filter_type == 'daily':
        today = timezone.now().date()
        transactions = transactions.filter(date=today)
    elif filter_type == 'monthly':
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        transactions = transactions.filter(date__gte=start_of_month, date__lte=today)
    
    context = {
        'transactions': transactions,
        'filter_type': filter_type,
        'transaction_type': 'income'
    }
    return render(request, 'finance/transaction_list.html', context)

@login_required
def expense_list(request):
    filter_type = request.GET.get('filter', 'all')
    transactions = Transaction.objects.filter(user=request.user, transaction_type='expense')
    
    if filter_type == 'daily':
        today = timezone.now().date()
        transactions = transactions.filter(date=today)
    elif filter_type == 'monthly':
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        transactions = transactions.filter(date__gte=start_of_month, date__lte=today)
    
    context = {
        'transactions': transactions,
        'filter_type': filter_type,
        'transaction_type': 'expense'
    }
    return render(request, 'finance/transaction_list.html', context)

@login_required
def add_income(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user, transaction_type='income')
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'income'
            transaction.save()
            messages.success(request, 'Income added successfully!')
            return redirect('income_list')
    else:
        form = TransactionForm(user=request.user, transaction_type='income')
    
    categories = Category.objects.filter(user=request.user, category_type='income')
    return render(request, 'finance/add_transaction.html', {
        'form': form, 
        'transaction_type': 'income',
        'categories': categories
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user, transaction_type='expense')
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'expense'
            transaction.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = TransactionForm(user=request.user, transaction_type='expense')
    
    categories = Category.objects.filter(user=request.user, category_type='expense')
    return render(request, 'finance/add_transaction.html', {
        'form': form, 
        'transaction_type': 'expense',
        'categories': categories
    })

@login_required
def add_category(request):
    category_type = request.GET.get('type', 'expense')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.category_type = category_type
            category.save()
            messages.success(request, f'{category_type.title()} category added successfully!')
            return redirect(f'add_{category_type}')
    else:
        form = CategoryForm()
    
    return render(request, 'finance/add_category.html', {
        'form': form,
        'category_type': category_type
    })

@login_required
def chart_data(request):
    # Expense breakdown by category
    expense_data = Transaction.objects.filter(
        user=request.user, 
        transaction_type='expense'
    ).values('category__name').annotate(total=Sum('amount'))
    
    # Income vs Expenses totals
    income_total = Transaction.objects.filter(
        user=request.user, 
        transaction_type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expense_total = Transaction.objects.filter(
        user=request.user, 
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    return JsonResponse({
        'expense_breakdown': list(expense_data),
        'income_vs_expense': {
            'income': float(income_total),
            'expense': float(expense_total)
        }
    })

# Set Monthly Budget view
from django.views.decorators.http import require_POST
from .models import MonthlyBudget
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
@login_required
@require_POST
def set_monthly_budget(request):
    budget = request.POST.get('budget')
    if budget:
        now = timezone.now()
        year = now.year
        month = now.month
        obj, created = MonthlyBudget.objects.update_or_create(
            user=request.user,
            year=year,
            month=month,
            defaults={'budget': budget}
        )
        messages.success(request, f"Monthly budget set to ₹{budget}")
    else:
        messages.error(request, "Please enter a valid budget amount.")
    return redirect('dashboard')
