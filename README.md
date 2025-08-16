# ERP Project

A comprehensive Django-based Enterprise Resource Planning (ERP) system with modules for Sales, Inventory, Accounting, HR, and User Management.

## Features

- **Sales Management**: Customer management, order processing, and invoicing
- **Inventory Management**: Product tracking, supplier management, and purchase orders
- **Accounting**: Ledger management, transactions, and financial reporting
- **HR Management**: Employee records, leave management, and attendance tracking
- **User Management**: Custom user authentication and authorization
- **Data Import/Export**: Export and import data in PDF and CSV formats across all modules

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Data Import/Export

The application supports exporting and importing data in PDF and CSV formats across all modules. Here's how to use these features:

### Exporting Data
1. Navigate to any list view (e.g., Products, Customers, Orders, Invoices, Employees)
2. Click the "Export" dropdown button
3. Select either "Export as PDF" or "Export as CSV"
4. The file will be automatically downloaded

### Importing Data
1. Navigate to any list view
2. Click the "Import" button
3. In the modal that appears, click "Choose File" and select your import file (PDF or CSV)
4. Click "Import" to upload and process the file
5. You'll see a success message once the import is complete

### Supported Data Types for Import/Export
- **Sales**: Customers, Orders, Invoices
- **Inventory**: Products, Suppliers, Purchase Orders
- **Accounting**: Ledgers, Transactions, Reports
- **HR**: Employees, Attendance, Leave records

## Testing

Run the test suite:
```bash
python run_tests.py
```

## Project Structure

```
erp_project/
├── accounting/          # Accounting module
├── hr/                 # Human Resources module
├── inventory/          # Inventory management module
├── sales/              # Sales management module
├── users/              # User management module
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── tests/              # Test files
└── erp_project/        # Django project settings
```

## Requirements

- Python 3.11+
- Django 4.2+
- SQLite (default) or PostgreSQL/MySQL for production
- Additional dependencies:
  - pandas (for data manipulation)
  - reportlab (for PDF generation)

## Configuration

The project uses environment variables for configuration. Create a `.env` file with:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Usage

1. Access the admin panel at `http://localhost:8000/admin/`
2. Use the dashboard at `http://localhost:8000/` for main functionality
3. Each module has its own URL patterns under respective paths
4. Use the export/import buttons in list views to manage your data

## Development

- Follow PEP 8 style guidelines
- Write tests for new features
- Use Django's built-in admin for data management
- Keep migrations up to date
- When adding new models, implement the necessary export/import methods

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is open source and available under the MIT License.
