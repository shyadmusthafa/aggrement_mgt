# Professional Email Management System

## Overview

The Professional Email Management System is a comprehensive email solution integrated into the Data Management System. It provides modern, professional email capabilities including template management, analytics, scheduling, and automated reminders.

## Features

### 🎨 **Professional UI Design**
- Modern, responsive design with gradient backgrounds
- Interactive cards and hover effects
- Professional color scheme (blue gradients)
- Mobile-responsive layout
- Smooth animations and transitions

### 📧 **Email Template Manager**
- **Template Creation**: Create custom email templates with variables
- **Template Editing**: Rich text editor with live preview
- **Variable System**: Dynamic placeholders for personalized content
- **Template Categories**: SPO Rent, CFA Agreement, Transporter, General
- **Preview Functionality**: Real-time template preview with sample data

### 📊 **Email Analytics Dashboard**
- **Key Metrics**: Delivery rate, open rate, click rate, bounce rate
- **Performance Charts**: Interactive charts showing email performance over time
- **Real-time Updates**: Live metric updates every 30 seconds
- **Filtering System**: Filter by date range, email type, recipient group, status
- **Export Options**: PDF, Excel, CSV export capabilities

### 🔄 **Email Composer**
- **Template Selection**: Choose from predefined templates
- **Recipient Management**: Select recipients by type or custom list
- **Scheduling**: Schedule emails for future delivery
- **Draft Saving**: Save email drafts for later editing
- **Variable Insertion**: Click-to-insert dynamic variables

### 📈 **Email History & Tracking**
- **Activity Feed**: Real-time email activity tracking
- **Status Monitoring**: Track sent, delivered, opened, clicked, failed emails
- **Search & Filter**: Advanced filtering and search capabilities
- **Export History**: Export email history and logs

## File Structure

```
dashboard/
├── templates/dashboard/
│   ├── mail_reminder.html          # Main email management page
│   ├── email_templates.html        # Template manager interface
│   └── email_analytics.html        # Analytics dashboard
├── views.py                        # Backend logic and views
└── urls.py                         # URL routing
```

## URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/mail-reminder/` | `mail_reminder` | Main email management dashboard |
| `/mail-reminder/templates/` | `email_templates` | Email template manager |
| `/mail-reminder/analytics/` | `email_analytics` | Email analytics dashboard |
| `/mail-reminder/test-email/` | `test_email_configuration` | Test email configuration |

## Email Templates

### Available Templates

1. **Renewal Reminder** (SPO Rent)
   - Purpose: Remind SPO partners about agreement renewals
   - Variables: `{{recipient_name}}`, `{{spo_name}}`, `{{spo_code}}`, `{{expiry_date}}`, `{{branch_name}}`, `{{monthly_rent}}`

2. **Expiry Notice** (CFA Agreement)
   - Purpose: Urgent notifications for expiring agreements
   - Variables: `{{recipient_name}}`, `{{cfa_name}}`, `{{agreement_number}}`, `{{expiry_date}}`, `{{branch_name}}`

3. **Payment Reminder** (General)
   - Purpose: Remind about outstanding payments
   - Variables: `{{recipient_name}}`, `{{amount}}`, `{{agreement_type}}`, `{{due_date}}`, `{{reference_number}}`

4. **Welcome Email** (General)
   - Purpose: Welcome new partners to the system
   - Variables: `{{recipient_name}}`, `{{username}}`, `{{email}}`, `{{role}}`

### Variable System

The email template system supports dynamic variables that are automatically replaced with actual data:

```html
Dear {{recipient_name}},

Your SPO Rent Agreement for {{spo_name}} (Code: {{spo_code}}) expires on {{expiry_date}}.

Branch: {{branch_name}}
Monthly Rent: ₹{{monthly_rent}}
```

## Analytics Features

### Key Metrics Tracked

1. **Total Emails Sent**: Count of all emails sent
2. **Delivery Rate**: Percentage of emails successfully delivered
3. **Open Rate**: Percentage of delivered emails opened
4. **Click Rate**: Percentage of opened emails with clicks
5. **Bounce Rate**: Percentage of emails that bounced
6. **Average Send Time**: Average time to send emails

### Chart Types

- **Performance Over Time**: Line charts showing metrics over time
- **Email Type Distribution**: Pie charts showing email type breakdown
- **Interactive Filters**: Filter data by date range, email type, recipient group

## Email Configuration

### SMTP Settings

The system is configured to use Chettinad's SMTP server:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.chettinad.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'chettinadsdc@chettinad.com'
EMAIL_HOST_PASSWORD = 'Raam@CheTTinaD2018'
DEFAULT_FROM_EMAIL = 'chettinadsdc@chettinad.com'
```

### Development Mode

For development, emails can be configured to output to console:

```python
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Usage Guide

### Creating Email Templates

1. Navigate to **Mail Reminder** → **Template Manager**
2. Click **Create New Template**
3. Fill in template details:
   - Template Name
   - Template Type
   - Subject Line
   - Email Content
4. Use variables by clicking on them in the variables panel
5. Preview the template with sample data
6. Save the template

### Sending Emails

1. Go to **Mail Reminder** → **Email Composer**
2. Select a template from the dropdown
3. Choose recipient type (SPO Rent, CFA Agreement, etc.)
4. Customize subject and content if needed
5. Schedule or send immediately
6. Monitor delivery status

### Viewing Analytics

1. Navigate to **Mail Reminder** → **Email Analytics**
2. View key metrics on the dashboard
3. Use filters to analyze specific data
4. Export reports in various formats
5. Schedule regular reports

## Technical Implementation

### Frontend Technologies

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript**: Interactive functionality and real-time updates
- **Font Awesome**: Professional icons
- **Responsive Design**: Mobile-first approach

### Backend Technologies

- **Django**: Web framework
- **Django Email**: Email sending functionality
- **SQLite**: Database (can be upgraded to PostgreSQL/MySQL)
- **ReportLab**: PDF generation for reports

### Key JavaScript Functions

```javascript
// Template Management
function selectTemplate(templateId)
function loadTemplateData(templateId)
function saveTemplate()
function previewTemplate()

// Email Composer
function sendEmail()
function scheduleEmail()
function loadRecipients()

// Analytics
function updateChart(chartType)
function applyFilters()
function exportAnalytics(format)
```

## Customization

### Adding New Templates

1. Add template data to the `templates` object in JavaScript
2. Create corresponding template item in the sidebar
3. Add any new variables to the variables panel
4. Update the backend email generation functions

### Customizing Styles

The system uses CSS custom properties for easy theming:

```css
:root {
    --primary-color: #3b82f6;
    --secondary-color: #1e40af;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
}
```

### Adding New Analytics Metrics

1. Add metric data to the backend
2. Update the analytics dashboard template
3. Add corresponding JavaScript functions
4. Update the export functionality

## Security Considerations

- All email views require login authentication
- CSRF protection enabled on all forms
- Email credentials stored securely in settings
- Input validation on all email content
- Rate limiting on email sending (recommended)

## Performance Optimization

- Database queries optimized with select_related
- Caching for frequently accessed data
- Lazy loading of email history
- Pagination for large datasets
- Asynchronous email sending (recommended)

## Future Enhancements

### Planned Features

1. **Advanced Scheduling**: Cron-based email scheduling
2. **A/B Testing**: Template performance testing
3. **Email Automation**: Workflow-based email sequences
4. **Advanced Analytics**: Machine learning insights
5. **API Integration**: Third-party email service integration
6. **Mobile App**: Native mobile application

### Technical Improvements

1. **Real-time Updates**: WebSocket integration for live updates
2. **Advanced Charts**: Chart.js or D3.js integration
3. **Email Tracking**: Pixel tracking and link tracking
4. **Bulk Operations**: Mass email operations
5. **Template Versioning**: Template history and rollback

## Troubleshooting

### Common Issues

1. **Emails Not Sending**
   - Check SMTP configuration
   - Verify email credentials
   - Check firewall settings

2. **Templates Not Loading**
   - Clear browser cache
   - Check JavaScript console for errors
   - Verify template data structure

3. **Analytics Not Updating**
   - Check database connectivity
   - Verify email tracking implementation
   - Check JavaScript errors

### Debug Mode

Enable debug mode to see detailed error messages:

```python
DEBUG = True
```

## Support

For technical support or feature requests, please contact the development team or create an issue in the project repository.

---

**Version**: 1.0.0  
**Last Updated**: July 2025  
**Compatibility**: Django 5.2+, Python 3.8+ 