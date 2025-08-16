from django.urls import path
from . import views

app_name = 'hr'  

urlpatterns = [
    # Employee URLs
    path('employees/', views.employees_list, name='employees_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/update/<int:pk>/', views.employee_update, name='employee_update'),
    path('employees/delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('employees/export/<str:format_type>/', views.export_employees, name='export_employees'),
    path('employees/import/', views.import_employees, name='import_employees'),
    
    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/update/<int:pk>/', views.attendance_update, name='attendance_update'),
    path('attendance/delete/<int:pk>/', views.attendance_delete, name='attendance_delete'),
    path('attendance/export/<str:format_type>/', views.export_attendance, name='export_attendance'),
    path('attendance/import/', views.import_attendance, name='import_attendance'),
    
    # Leave URLs
    path('leaves/', views.leaves_list, name='leaves_list'),
    path('leaves/create/', views.leave_create, name='leave_create'),
    path('leaves/update/<int:pk>/', views.leave_update, name='leave_update'),
    path('leaves/delete/<int:pk>/', views.leave_delete, name='leave_delete'),
    path('leaves/export/<str:format_type>/', views.export_leaves, name='export_leaves'),
    path('leaves/import/', views.import_leaves, name='import_leaves'),
]
