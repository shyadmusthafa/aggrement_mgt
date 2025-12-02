# Data Management System - Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Features](#features)
4. [Installation & Setup](#installation--setup)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [User Management](#user-management)
8. [Approval Workflow](#approval-workflow)
9. [Email Notifications](#email-notifications)
10. [Menu Access Control](#menu-access-control)
11. [Usage Guide](#usage-guide)
12. [Troubleshooting](#troubleshooting)
13. [Development Guide](#development-guide)

## Project Overview

The Data Management System is a comprehensive Django-based web application designed to manage SPO (Storage Point of Origin), CFA (Central Freight Agency), and Transporter agreements. The system provides a robust approval workflow, user management, and comprehensive data tracking capabilities.

### Key Objectives
- Centralized management of business agreements
- Streamlined approval workflows
- Comprehensive user access control
- Automated email notifications
- Data integrity and validation

## System Architecture

### Technology Stack
- **Backend**: Django 5.2.4
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Django's built-in authentication system
- **Email**: Django EmailMessage with HTML templates

### Project Structure
```
Data Management/
├── dashboard/                 # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   ├── forms.py             # Form definitions
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin interface
│   └── templates/           # HTML templates
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── PROJECT_DOCUMENTATION.md  # This file
```

## Features

### 1. Core Data Management
- **SPO Rent Management**: Storage Point of Origin rental agreements
- **CFA Agreement Management**: Central Freight Agency agreements
- **Transporter Agreement Management**: Transportation service agreements
- **Partner Management**: Associate partner details for each agreement

### 2. Approval Workflow System
- **Multi-level Approval**: Superior confirmation workflow
- **Status Tracking**: Waiting → Confirmed workflow states
- **Approval Dashboard**: Centralized approval management
- **History Tracking**: Complete audit trail of approvals

### 3. User Management System
- **User Registration**: Custom user creation with role assignment
- **Password Management**: Secure password reset functionality
- **Role-based Access**: Granular permission system
- **Menu Access Control**: Dynamic menu item permissions

### 4. Advanced Features
- **Dynamic Form Loading**: AJAX-based state/branch/district cascading
- **File Upload**: Document management with size validation
- **Email Notifications**: Automated approval notifications
- **Data Export**: CSV export functionality
- **Search & Filter**: Advanced data filtering capabilities

## Installation & Setup

### Prerequisites
- Python 3.13+
- MySQL 8.0+
- pip (Python package manager)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd "Data Management"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Database Configuration
1. Create MySQL database
2. Update `settings.py` with database credentials
3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 5: Run Development Server
```bash
python manage.py runserver
```

## Database Schema

### Core Models

#### SPORent Model
```python
class SPORent(models.Model):
    # Basic Information
    state = models.ForeignKey(MasState, on_delete=models.CASCADE)
    branch = models.ForeignKey(MasStateBranch, on_delete=models.CASCADE)
    district = models.ForeignKey(MasDistrict, on_delete=models.SET_NULL)
    district_code = models.CharField(max_length=20)
    spo_code = models.CharField(max_length=50, unique=True)
    spo_name = models.CharField(max_length=200)
    
    # Business Details
    stru_grp = models.CharField(max_length=20, choices=STRUCTURE_GROUPS)
    cfa_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    inception_date = models.DateField()
    
    # Financial Information
    security_deposit_paid = models.DecimalField(max_digits=10, decimal_places=2)
    rent_pm = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_hike_percent = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
```

#### MasDistrict Model
```python
class MasDistrict(models.Model):
    mas_state = models.ForeignKey(MasState, on_delete=models.CASCADE)
    mas_branch = models.ForeignKey(MasStateBranch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    status = models.IntegerField(default=1, choices=[(1, 'Active'), (0, 'Inactive')])
```

#### Approval Workflow Models
```python
class ApprovalWorkflow(models.Model):
    record_type = models.CharField(max_length=50)  # 'spo_rent', 'cfa_agreement', 'transporter_agreement'
    record_id = models.IntegerField()
    status = models.CharField(max_length=50, default='Waiting for Superior Confirmation')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
```

### Database Relationships
- **MasState** → **MasStateBranch** (One-to-Many)
- **MasStateBranch** → **MasDistrict** (One-to-Many)
- **SPORent** → **MasDistrict** (Many-to-One)
- **User** → **ApprovalWorkflow** (One-to-Many)

## API Endpoints

### AJAX Endpoints

#### Get Branches by State
```
GET /dashboard/get-branches-by-state/?state_id={id}
Response: {"branches": [{"id": 1, "state_branch_name": "Branch Name", "state_branch_code": "BC001"}]}
```

#### Get Districts by Branch
```
GET /dashboard/get-districts-by-branch/?state_id={id}&branch_id={id}
Response: {"districts": [{"id": 1, "name": "District Name", "code": "DC001"}]}
```

### Main Application URLs
- **SPO Management**: `/dashboard/spo-rent/`
- **CFA Management**: `/dashboard/cfa-agreement/`
- **Transporter Management**: `/dashboard/transporter-agreement/`
- **Approval Dashboard**: `/dashboard/approval-workflow/`
- **User Management**: `/dashboard/user-management/`
- **Menu Access Control**: `/dashboard/menu-access/`

## User Management

### User Roles
1. **Superuser**: Full system access
2. **Staff Users**: Limited administrative access
3. **Regular Users**: Basic data entry and viewing

### Permission System
- **can_view**: View records
- **can_create**: Create new records
- **can_edit**: Modify existing records
- **can_delete**: Remove records
- **can_approve**: Approve workflow items

### User Creation Process
1. Admin creates user account
2. Assigns appropriate roles
3. Configures menu access permissions
4. User receives login credentials

## Approval Workflow

### Workflow States
1. **Waiting for Superior Confirmation**: Initial state for new records
2. **Confirmed**: Approved by superior
3. **Rejected**: Declined with remarks

### Approval Process
1. User creates new record (SPO/CFA/Transporter)
2. Record automatically enters approval workflow
3. Superior reviews record details
4. Superior approves/rejects with remarks
5. Record status updated accordingly
6. Email notification sent to relevant parties

### Approval Dashboard Features
- **Pending Approvals**: List of records awaiting approval
- **Approval History**: Complete audit trail
- **Bulk Operations**: Process multiple approvals
- **Filtering**: Search by record type, date, status

## Email Notifications

### Email Templates
- **SPO Creation Notification**: New SPO record created
- **CFA Creation Notification**: New CFA agreement created
- **Transporter Creation Notification**: New transporter agreement created
- **Approval Notifications**: Status change notifications

### Email Features
- **HTML Templates**: Professional, branded email design
- **Dynamic Content**: Personalized with record details
- **Attachment Support**: Include relevant documents
- **Responsive Design**: Mobile-friendly email layout

## Menu Access Control

### Menu Structure
- **Dashboard**: Main navigation hub
- **Data Management**: SPO, CFA, Transporter modules
- **Approval System**: Workflow management
- **Administration**: User and system management
- **Reports**: Data analytics and exports

### Access Control Implementation
```python
class UserMenuAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=True)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_approve = models.BooleanField(default=False)
```

## Usage Guide

### Creating SPO Records
1. Navigate to SPO Rent → Add New
2. Select State → Branch → District (cascading dropdowns)
3. Fill in SPO details (name, code, structure group)
4. Enter financial information (rent, security deposit)
5. Upload required documents
6. Submit for approval

### Managing Approvals
1. Access Approval Workflow Dashboard
2. Review pending records
3. Click on record to view details
4. Add approval remarks
5. Approve or reject record
6. System updates status and sends notifications

### User Management
1. Access Administration → User Management
2. Create new user accounts
3. Assign roles and permissions
4. Configure menu access
5. Set password policies

## Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Check MySQL service status
sudo systemctl status mysql

# Verify database credentials in settings.py
# Ensure database exists and is accessible
```

#### Migration Issues
```bash
# Reset migrations if needed
python manage.py migrate --fake-initial

# Check migration status
python manage.py showmigrations
```

#### Form Validation Errors
- Verify field choices in models
- Check form field requirements
- Ensure proper foreign key relationships

#### AJAX Loading Issues
- Check browser console for JavaScript errors
- Verify URL patterns in urls.py
- Ensure proper CSRF token handling

### Debug Mode
```python
# In settings.py
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Enable logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

## Development Guide

### Adding New Models
1. Define model in `models.py`
2. Create form in `forms.py`
3. Add views in `views.py`
4. Configure URLs in `urls.py`
5. Create templates in `templates/`
6. Register in `admin.py`
7. Create and run migrations

### Customizing Forms
```python
class CustomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom field configuration
        self.fields['field_name'].queryset = Model.objects.filter(condition)
        self.fields['field_name'].widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        # Custom validation logic
        return cleaned_data
```

### Adding AJAX Functionality
```javascript
// JavaScript for dynamic loading
function loadData(url, params) {
    fetch(url + '?' + new URLSearchParams(params))
        .then(response => response.json())
        .then(data => {
            // Handle response data
        })
        .catch(error => console.error('Error:', error));
}
```

### Testing
```bash
# Run tests
python manage.py test

# Run specific test
python manage.py test dashboard.tests.TestModel

# Check test coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Production Settings
```python
# In settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'production_db',
        'USER': 'db_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Server Requirements
- **Web Server**: Nginx or Apache
- **Application Server**: Gunicorn or uWSGI
- **Database**: MySQL 8.0+
- **Python**: 3.13+
- **Memory**: Minimum 2GB RAM
- **Storage**: Minimum 10GB disk space

## Support & Maintenance

### Regular Maintenance Tasks
1. **Database Backup**: Daily automated backups
2. **Log Rotation**: Weekly log file management
3. **Security Updates**: Monthly security patches
4. **Performance Monitoring**: Continuous system monitoring

### Backup Strategy
```bash
# Database backup
mysqldump -u username -p database_name > backup_$(date +%Y%m%d).sql

# File backup
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### Monitoring
- **Application Logs**: Django logging system
- **Database Performance**: MySQL slow query log
- **Server Resources**: CPU, memory, disk usage
- **Error Tracking**: Django error reporting

---

## Conclusion

This Data Management System provides a robust, scalable solution for managing business agreements and workflows. The system's modular architecture allows for easy extension and customization while maintaining data integrity and security.

For additional support or feature requests, please contact the development team or refer to the project repository for the latest updates and documentation.

---

**Document Version**: 1.0  
**Last Updated**: August 2025  
**Maintained By**: Development Team
