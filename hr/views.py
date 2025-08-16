from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Employee, Attendance, Leave
from .forms import EmployeeForm, AttendanceForm, LeaveForm
from erp_project.export_import_utils import export_to_csv, export_to_pdf, import_from_csv

# Employee Views
def employees_list(request):
    employees = Employee.objects.all()
    return render(request, 'hr/employees.html', {'employees': employees})

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm()
    return render(request, 'hr/employee_form.html', {'form': form})

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'hr/employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('employees_list')

# Attendance Views
def attendance_list(request):
    attendance = Attendance.objects.all()
    return render(request, 'hr/attendance.html', {'attendance': attendance})

def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'hr/attendance_form.html', {'form': form})

def attendance_update(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'hr/attendance_form.html', {'form': form})

def attendance_delete(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.delete()
    return redirect('attendance_list')

# Leave Views
def leaves_list(request):
    leaves = Leave.objects.all()
    return render(request, 'hr/leaves.html', {'leaves': leaves})

def leave_create(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leaves_list')
    else:
        form = LeaveForm()
    return render(request, 'hr/leave_form.html', {'form': form})

def leave_update(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leaves_list')
    else:
        form = LeaveForm(instance=leave)
    return render(request, 'hr/leave_form.html', {'form': form})

def leave_delete(request, pk):
    leave = get_object_or_404(Leave, pk=pk)
    leave.delete()
    return redirect('leaves_list')

# Export/Import Views
def export_employees(request, format_type='csv'):
    fields = ['id', 'name', 'email', 'phone', 'position', 'hire_date', 'created_at']
    employees = Employee.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('employees', employees, fields, 'Employees List')
    else:
        return export_to_csv('employees', employees, fields)

def export_attendance(request, format_type='csv'):
    fields = ['id', 'employee__name', 'date', 'status']
    attendance = Attendance.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('attendance', attendance, fields, 'Attendance Records')
    else:
        return export_to_csv('attendance', attendance, fields)

def export_leaves(request, format_type='csv'):
    fields = ['id', 'employee__name', 'start_date', 'end_date', 'reason']
    leaves = Leave.objects.all()
    
    if format_type == 'pdf':
        return export_to_pdf('leaves', leaves, fields, 'Leave Records')
    else:
        return export_to_csv('leaves', leaves, fields)

@require_http_methods(["POST"])
def import_employees(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('employees_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Name': 'name',
        'Email': 'email',
        'Phone': 'phone',
        'Position': 'position',
        'Hire Date': 'hire_date'
    }
    
    success, message = import_from_csv(Employee, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('employees_list')

@require_http_methods(["POST"])
def import_attendance(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('attendance_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Employee': 'employee',
        'Date': 'date',
        'Status': 'status'
    }
    
    success, message = import_from_csv(Attendance, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('attendance_list')

@require_http_methods(["POST"])
def import_leaves(request):
    if 'file' not in request.FILES:
        messages.error(request, 'No file was uploaded.')
        return redirect('leaves_list')
    
    file = request.FILES['file']
    field_mapping = {
        'Employee': 'employee',
        'Start Date': 'start_date',
        'End Date': 'end_date',
        'Reason': 'reason'
    }
    
    success, message = import_from_csv(Leave, file, field_mapping)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('leaves_list')
