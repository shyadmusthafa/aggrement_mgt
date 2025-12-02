from .models import UserMenuAccess
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def user_menu_access(request):
    """Context processor to make user menu access available in all templates"""
    if request.user.is_authenticated:
        try:
            menu_access = UserMenuAccess.objects.get(user=request.user)
            logger.info(f"Menu access found for user {request.user.username}: SPO={menu_access.spo_menu_enabled}, CFA={menu_access.cfa_menu_enabled}, Transport={menu_access.transport_menu_enabled}, Approval={menu_access.approval_menu_enabled}, ApprovalWorkflow={menu_access.approval_workflow_enabled}, Report={menu_access.report_enabled}, MailReminder={menu_access.mail_reminder_enabled}, UserManagement={menu_access.user_management_enabled}, UserMenuAccessControl={menu_access.user_menu_access_control_enabled}")
            return {
                'user_menu_access': {
                    'spo_menu_enabled': menu_access.spo_menu_enabled,
                    'cfa_menu_enabled': menu_access.cfa_menu_enabled,
                    'transport_menu_enabled': menu_access.transport_menu_enabled,
                    'approval_menu_enabled': menu_access.approval_menu_enabled,
                    'approval_workflow_enabled': menu_access.approval_workflow_enabled,
                    'report_enabled': menu_access.report_enabled,
                    'mail_reminder_enabled': menu_access.mail_reminder_enabled,
                    'user_management_enabled': menu_access.user_management_enabled,
                    'user_menu_access_control_enabled': menu_access.user_menu_access_control_enabled,
                }
            }
        except UserMenuAccess.DoesNotExist:
            # If no menu access record exists, return False for all menus
            # This ensures users without explicit permissions cannot access restricted menus
            logger.warning(f"No menu access record found for user {request.user.username}, denying all access")
            return {
                'user_menu_access': {
                    'spo_menu_enabled': False,
                    'cfa_menu_enabled': False,
                    'transport_menu_enabled': False,
                    'approval_menu_enabled': False,
                    'approval_workflow_enabled': False,
                    'report_enabled': False,
                    'mail_reminder_enabled': False,
                    'user_management_enabled': False,
                    'user_menu_access_control_enabled': False,
                }
            }
    else:
        logger.info("User not authenticated, returning no menu access")
    return {'user_menu_access': None}

def debug_context(request):
    """Context processor to make debug variable available in templates"""
    return {'debug': settings.DEBUG}

def current_time_context(request):
    """Context processor to add current time for debugging template caching"""
    return {'now': timezone.now()}
