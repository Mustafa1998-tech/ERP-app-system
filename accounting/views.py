from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Ledger, Transaction, Report
from .forms import LedgerForm, TransactionForm, ReportForm
from erp_project.export_import_utils import export_to_csv, export_to_pdf, import_from_csv

def dashboard(request):
    """Display the accounting dashboard."""
    context = {
        'total_ledgers': Ledger.objects.count(),
        'total_transactions': Transaction.objects.count(),
        'total_reports': Report.objects.count(),
    }
    return render(request, 'accounting/dashboard.html', context)

# Ledger Views
def ledgers_list(request):
    ledgers = Ledger.objects.all()
    return render(request, 'accounting/ledgers.html', {'ledgers': ledgers})

def ledger_create(request):
    if request.method == 'POST':
        form = LedgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ledgers_list')
    else:
        form = LedgerForm()
    return render(request, 'accounting/ledger_form.html', {'form': form})

def ledger_update(request, pk):
    ledger = get_object_or_404(Ledger, pk=pk)
    if request.method == 'POST':
        form = LedgerForm(request.POST, instance=ledger)
        if form.is_valid():
            form.save()
            return redirect('ledgers_list')
    else:
        form = LedgerForm(instance=ledger)
    return render(request, 'accounting/ledger_form.html', {'form': form})

def ledger_delete(request, pk):
    ledger = get_object_or_404(Ledger, pk=pk)
    ledger.delete()
    return redirect('ledgers_list')

# Transaction Views
def transactions_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'accounting/transactions.html', {'transactions': transactions})

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions_list')
    else:
        form = TransactionForm()
    return render(request, 'accounting/transaction_form.html', {'form': form})

def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transactions_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'accounting/transaction_form.html', {'form': form})

def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return redirect('transactions_list')

# Report Views
def reports_list(request):
    reports = Report.objects.all()
    return render(request, 'accounting/reports.html', {'reports': reports})

def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reports_list')
    else:
        form = ReportForm()
    return render(request, 'accounting/report_form.html', {'form': form})

def report_update(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('reports_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'accounting/report_form.html', {'form': form})

def report_delete(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.delete()
    return redirect('reports_list')

def report_generate(request, report_type):
    """
    Generate different types of financial reports.
    Supported report types: trial_balance, income_statement, balance_sheet, cash_flow
    """
    from django.db.models import Sum, Q
    from decimal import Decimal
    from datetime import datetime, timedelta
    
    context = {
        'report_type': report_type,
        'generated_date': datetime.now(),
    }
    
    # Common date range for reports (last 30 days by default)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    if report_type == 'trial_balance':
        # Calculate trial balance (debits and credits for each ledger)
        ledgers = Ledger.objects.annotate(
            total_debit=Sum('transaction__amount', 
                          filter=Q(transaction__transaction_type='expense',
                                 transaction__date__range=[start_date, end_date]),
                          default=0),
            total_credit=Sum('transaction__amount',
                           filter=Q(transaction__transaction_type='income',
                                  transaction__date__range=[start_date, end_date]),
                           default=0)
        )
        
        # Calculate the difference (balance) for each ledger
        ledgers = [
            {
                'name': ledger.name,
                'debit': ledger.total_debit or 0,
                'credit': ledger.total_credit or 0,
                'balance': (ledger.total_credit or 0) - (ledger.total_debit or 0)
            }
            for ledger in ledgers
        ]
        
        context.update({
            'ledgers': ledgers,
            'start_date': start_date,
            'end_date': end_date,
            'total_debit': sum(ledger['debit'] for ledger in ledgers),
            'total_credit': sum(ledger['credit'] for ledger in ledgers),
            'total_balance': sum(ledger['balance'] for ledger in ledgers),
        })
        
    elif report_type == 'income_statement':
        # Calculate revenue and expenses
        revenue = Transaction.objects.filter(
            ledger__type='revenue',
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        expenses = Transaction.objects.filter(
            ledger__type='expense',
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        context.update({
            'revenue': revenue,
            'expenses': expenses,
            'net_income': revenue - expenses,
            'start_date': start_date,
            'end_date': end_date,
        })
        
    elif report_type == 'balance_sheet':
        # Calculate assets, liabilities, and equity
        assets = Transaction.objects.filter(
            ledger__type='asset',
            date__lte=end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        liabilities = Transaction.objects.filter(
            ledger__type='liability',
            date__lte=end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        equity = Transaction.objects.filter(
            ledger__type='equity',
            date__lte=end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        context.update({
            'assets': assets,
            'liabilities': liabilities,
            'equity': equity,
            'report_date': end_date,
        })
    
    elif report_type == 'cash_flow':
        # Calculate cash flow from operating, investing, and financing activities
        operating = Transaction.objects.filter(
            Q(ledger__type='revenue') | Q(ledger__type='expense'),
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        investing = Transaction.objects.filter(
            ledger__type='asset',
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        financing = Transaction.objects.filter(
            Q(ledger__type='liability') | Q(ledger__type='equity'),
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        context.update({
            'operating_cash_flow': operating,
            'investing_cash_flow': investing,
            'financing_cash_flow': financing,
            'net_cash_flow': operating + investing + financing,
            'start_date': start_date,
            'end_date': end_date,
        })
    else:
        # Handle unknown report type
        from django.http import Http404
        raise Http404("Report type not found")
    
    return render(request, f'accounting/reports/{report_type}.html', context)

def test_template(request):
    """Test view to verify template loading."""
    return render(request, 'accounting/test_template.html')

# Export/Import Views for Accounting

def export_ledgers(request, format_type='csv'):
    fields = ['id', 'name', 'description', 'created_at']
    ledgers = Ledger.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('ledgers', ledgers, fields, 'Ledgers List')
    else:
        return export_to_csv('ledgers', ledgers, fields)

def export_transactions(request, format_type='csv'):
    fields = ['id', 'ledger__name', 'date', 'amount', 'description', 'transaction_type', 'created_at']
    transactions = Transaction.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('transactions', transactions, fields, 'Transactions List')
    else:
        return export_to_csv('transactions', transactions, fields)

def export_reports(request, format_type='csv'):
    fields = ['id', 'title', 'content', 'created_at']
    reports = Report.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('reports', reports, fields, 'Reports List')
    else:
        return export_to_csv('reports', reports, fields)

@require_http_methods(["POST"])
def import_ledgers(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('accounting:ledgers_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Name': 'name',
        'Description': 'description'
    }
    
    success, message = import_from_csv(Ledger, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('accounting:ledgers_list')

@require_http_methods(["POST"])
def import_transactions(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('accounting:transactions_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Ledger': 'ledger',
        'Date': 'date',
        'Amount': 'amount',
        'Description': 'description',
        'Transaction Type': 'transaction_type'
    }
    
    success, message = import_from_csv(Transaction, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('accounting:transactions_list')

@require_http_methods(["POST"])
def import_reports(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('accounting:reports_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Title': 'title',
        'Content': 'content'
    }
    
    success, message = import_from_csv(Report, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('accounting:reports_list')
