from django import template
import os

register = template.Library()

@register.filter
def get_field_label(form, field_name):
    """
    Get the label for a form field
    """
    if field_name in form.fields:
        return form.fields[field_name].label or field_name.replace('_', ' ').title()
    return field_name.replace('_', ' ').title()

@register.filter
def get_filename(file_path):
    """
    Get the filename from a file path
    """
    if file_path:
        return os.path.basename(str(file_path))
    return '' 