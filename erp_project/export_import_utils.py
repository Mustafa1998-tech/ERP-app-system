import csv
import io
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def export_to_csv(model_name, queryset, fields):
    """
    Generic function to export data to CSV
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename=\"{model_name}_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(fields)
    
    for obj in queryset:
        row = []
        for field in fields:
            if '__' in field:  # Handle related fields
                related_fields = field.split('__')
                value = obj
                for f in related_fields:
                    value = getattr(value, f, '')
                row.append(str(value) if value is not None else '')
            else:
                value = getattr(obj, field, '')
                row.append(str(value) if value is not None else '')
        writer.writerow(row)
    
    return response

def export_to_pdf(model_name, data, fields, title):
    """
    Generic function to export data to PDF
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=\"{model_name}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        spaceAfter=30
    )
    elements.append(Paragraph(title, title_style))
    
    # Prepare data for table
    table_data = [fields]
    for item in data:
        row = []
        for field in fields:
            if '__' in field:  # Handle related fields
                related_fields = field.split('__')
                value = item
                for f in related_fields:
                    value = getattr(value, f, '')
                row.append(str(value) if value is not None else '')
            else:
                value = getattr(item, field, '')
                row.append(str(value) if value is not None else '')
        table_data.append(row)
    
    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    return response

def import_from_csv(model, file, field_mapping):
    """
    Generic function to import data from CSV
    """
    try:
        # Read the CSV file
        csv_file = io.TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        
        # Process each row
        created_count = 0
        updated_count = 0
        
        for row in reader:
            # Map CSV columns to model fields
            data = {}
            for csv_field, model_field in field_mapping.items():
                if csv_field in row:
                    data[model_field] = row[csv_field]
            
            # Create or update the object
            if 'id' in data and data['id']:
                # Update existing object
                obj, created = model.objects.update_or_create(
                    id=data['id'],
                    defaults=data
                )
                if not created:
                    updated_count += 1
            else:
                # Create new object
                model.objects.create(**data)
                created_count += 1
        
        return True, f"Successfully imported {created_count} new records and updated {updated_count} records."
    except Exception as e:
        return False, f"Error during import: {str(e)}"
