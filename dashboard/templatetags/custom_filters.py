from django import template

register = template.Library()

@register.filter
def status_color(status):
    """
    Returns Bootstrap color class based on status value
    """
    if not status:
        return 'secondary'
    
    status = str(status).lower()
    
    # Define status to color mapping
    status_colors = {
        'active': 'success',
        'inactive': 'danger',
        'suspended': 'warning',
        'terminated': 'dark',
        'waiting for superior confirmation': 'info',
        'confirmed': 'success',
        'rejected': 'danger',
        'pending': 'warning',
        'completed': 'success',
        'cancelled': 'secondary',
        'draft': 'light',
        'submitted': 'primary',
        'approved': 'success',
        'declined': 'danger',
        'under review': 'info',
        'processing': 'warning',
        'sent': 'success',
        'failed': 'danger',
        'delivered': 'success',
        'read': 'info',
        'unread': 'warning',
    }
    
    return status_colors.get(status, 'secondary')

@register.filter
def status_icon(status):
    """
    Returns FontAwesome icon class based on status value
    """
    if not status:
        return 'fa-question-circle'
    
    status = str(status).lower()
    
    # Define status to icon mapping
    status_icons = {
        'active': 'fa-check-circle',
        'inactive': 'fa-times-circle',
        'suspended': 'fa-pause-circle',
        'terminated': 'fa-ban',
        'waiting for superior confirmation': 'fa-clock',
        'confirmed': 'fa-check-circle',
        'rejected': 'fa-times-circle',
        'pending': 'fa-hourglass-half',
        'completed': 'fa-check-circle',
        'cancelled': 'fa-times',
        'draft': 'fa-edit',
        'submitted': 'fa-paper-plane',
        'approved': 'fa-thumbs-up',
        'declined': 'fa-thumbs-down',
        'under review': 'fa-search',
        'processing': 'fa-cog',
        'sent': 'fa-paper-plane',
        'failed': 'fa-exclamation-triangle',
        'delivered': 'fa-inbox',
        'read': 'fa-eye',
        'unread': 'fa-envelope',
    }
    
    return status_icons.get(status, 'fa-question-circle')

@register.filter
def truncate_words(value, arg):
    """
    Truncates a string after a certain number of words
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    
    words = value.split()
    if len(words) <= length:
        return value
    
    return ' '.join(words[:length]) + '...'

@register.filter
def format_currency(value):
    """
    Formats a number as currency
    """
    try:
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return value

@register.filter
def format_date(value):
    """
    Formats a date in a readable format
    """
    if value:
        return value.strftime("%d %b %Y")
    return ""

@register.filter
def format_datetime(value):
    """
    Formats a datetime in a readable format
    """
    if value:
        return value.strftime("%d %b %Y %I:%M %p")
    return ""

@register.filter
def get_item(dictionary, key):
    """
    Gets an item from a dictionary using a key
    """
    return dictionary.get(key)

@register.filter
def get_menu_status(user_menu_access, user_id):
    """Get menu status for a specific user"""
    if user_id in user_menu_access:
        return user_menu_access[user_id]
    return {}

@register.filter
def add_class(field, css_class):
    """
    Adds a CSS class to a form field
    """
    return field.as_widget(attrs={"class": css_class})

@register.filter
def is_list(value):
    """
    Checks if a value is a list
    """
    return isinstance(value, list)

@register.filter
def is_dict(value):
    """
    Checks if a value is a dictionary
    """
    return isinstance(value, dict)

@register.filter
def get_field_label(form, field_name):
    """
    Returns the label for a form field
    """
    if field_name in form.fields:
        return form.fields[field_name].label or field_name.replace('_', ' ').title()
    return field_name.replace('_', ' ').title()
