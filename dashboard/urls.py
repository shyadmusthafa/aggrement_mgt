from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/view/<int:user_id>/', views.view_user, name='view_user'),
    path('users/reset-password/<int:user_id>/', views.reset_user_password, name='reset_user_password'),
    path('users/change-password/', views.change_password, name='change_password'),
    
    # Simple User Menu Control URLs
    path('menu-access/', views.menu_access_dashboard, name='menu_access_dashboard'),
    path('menu-access/update/', views.update_user_menu_access, name='update_user_menu_access'),

    
    # MasDistrict URLs
    path('mas-district/', views.mas_district_list, name='mas_district_list'),
    path('mas-district/create/', views.mas_district_create, name='mas_district_create'),
    path('mas-district/edit/<int:district_id>/', views.mas_district_edit, name='mas_district_edit'),
    path('mas-district/delete/<int:district_id>/', views.mas_district_delete, name='mas_district_delete'),
            path('mas-district/get-branches/', views.get_branches_by_state, name='get_branches_by_state'),
        path('get-districts-by-branch/', views.get_districts_by_branch, name='get_districts_by_branch'),
        path('get-districts-by-state/', views.get_districts_by_state, name='get_districts_by_state'),
        path('get-district-details/', views.get_district_details, name='get_district_details'),
    
    # SPO Rent URLs
    path('spo-rent/', views.spo_rent_list, name='spo_rent_list'),
    path('spo-rent/export-excel/', views.spo_rent_export_excel, name='spo_rent_export_excel'),
    path('spo-rent/add/', views.spo_rent_create, name='spo_rent_create'),
    path('spo-rent/edit/<int:record_id>/', views.spo_rent_edit, name='spo_rent_edit'),
    path('spo-rent/view/<int:record_id>/', views.spo_rent_view, name='spo_rent_view'),
    path('spo-rent/delete/<int:record_id>/', views.spo_rent_delete, name='spo_rent_delete'),
    path('spo-rent/pdf/<int:record_id>/', views.spo_rent_pdf, name='spo_rent_pdf'),
    
    # CFA Agreement URLs
    path('cfa-agreement/', views.cfa_agreement_list, name='cfa_agreement_list'),
    path('cfa-agreement/export-excel/', views.cfa_agreement_export_excel, name='cfa_agreement_export_excel'),
    path('cfa-agreement/create/', views.cfa_agreement_create, name='cfa_agreement_create'),
    path('cfa-agreement/edit/<int:cfa_id>/', views.cfa_agreement_edit, name='cfa_agreement_edit'),
    path('cfa-agreement/view/<int:cfa_id>/', views.cfa_agreement_view, name='cfa_agreement_view'),
    path('cfa-agreement/pdf/<int:cfa_id>/', views.cfa_agreement_pdf, name='cfa_agreement_pdf'),
    path('cfa-agreement/delete/<int:cfa_id>/', views.cfa_agreement_delete, name='cfa_agreement_delete'),
    
    # Transporter Agreement URLs
    path('transporter-agreement/', views.transporter_agreement_list, name='transporter_agreement_list'),
    path('transporter-agreement/export-excel/', views.transporter_agreement_export_excel, name='transporter_agreement_export_excel'),
    path('transporter-agreement/create/', views.transporter_agreement_create, name='transporter_agreement_create'),
    path('transporter-agreement/edit/<int:transporter_id>/', views.transporter_agreement_edit, name='transporter_agreement_edit'),
    path('transporter-agreement/view/<int:transporter_id>/', views.transporter_agreement_view, name='transporter_agreement_view'),
    path('transporter-agreement/pdf/<int:transporter_id>/', views.transporter_agreement_pdf, name='transporter_agreement_pdf'),
    path('transporter-agreement/delete/<int:transporter_id>/', views.transporter_agreement_delete, name='transporter_agreement_delete'),
    
    # Approvals URLs
    path('approvals/', views.approval_list, name='approval_list'),
    path('approvals/export-excel/', views.approval_export_excel, name='approval_export_excel'),
    path('approvals/create/', views.approval_create, name='approval_create'),
    path('approvals/edit/<int:approval_id>/', views.approval_edit, name='approval_edit'),
    path('approvals/view/<int:approval_id>/', views.approval_view, name='approval_view'),
    path('approvals/delete/<int:approval_id>/', views.approval_delete, name='approval_delete'),
    path('approvals/approve/<int:approval_id>/', views.approval_approve, name='approval_approve'),
    path('approvals/reject/<int:approval_id>/', views.approval_reject, name='approval_reject'),
    path('approvals/pdf/<int:approval_id>/', views.approval_pdf, name='approval_pdf'),
    
    # Reports URLs
    path('reports/', views.reports, name='reports'),
    
    # Mail Reminder URLs
    path('mail-reminder/', views.mail_reminder, name='mail_reminder'),
    path('mail-reminder/templates/', views.email_templates, name='email_templates'),
    path('mail-reminder/analytics/', views.email_analytics, name='email_analytics'),
    path('mail-reminder/spo-rent/', views.spo_rent_reminder, name='spo_rent_reminder'),
    path('mail-reminder/spo-rent/send-email/', views.send_spo_rent_email, name='send_spo_rent_email'),
    path('mail-reminder/send-spo-reminder/', views.send_spo_reminder_mail, name='send_spo_reminder_mail'),
            path('mail-reminder/test-email/', views.test_email_configuration, name='test_email_configuration'),
        path('mail-reminder/test-ui/', views.test_email_ui, name='test_email_ui'),
    path('mail-reminder/cfa/', views.cfa_reminder, name='cfa_reminder'),
    path('mail-reminder/transporter/', views.transporter_reminder, name='transporter_reminder'),
    path('mail-reminder/payment/', views.payment_reminder, name='payment_reminder'),
    path('mail-reminder/document/', views.document_reminder, name='document_reminder'),
    
    # AJAX URLs for dynamic dropdowns
    path('ajax/load-branches/', views.load_branches, name='load_branches'),
    path('ajax/load-branches-cfa/', views.load_branches_for_cfa, name='load_branches_for_cfa'),
    path('ajax/load-branches-transporter/', views.load_branches_for_transporter, name='load_branches_for_transporter'),
    path('ajax/get-branch-details/', views.get_branch_details, name='get_branch_details'),
    
    # Approval Workflow URLs
    path('approval-workflow/', views.approval_workflow_dashboard, name='approval_workflow_dashboard'),
    path('approval-workflow/<int:workflow_id>/', views.approval_workflow_detail, name='approval_workflow_detail'),
    path('approval-workflow/<int:workflow_id>/approve/', views.approval_workflow_approve, name='approval_workflow_approve'),
    path('approval-workflow/<int:workflow_id>/reject/', views.approval_workflow_reject, name='approval_workflow_reject'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('ajax/workflow-status/<str:record_type>/<int:record_id>/', views.get_workflow_status, name='get_workflow_status'),
    path('ajax/spo-records/', views.spo_records_ajax, name='spo_records_ajax'),
    path('ajax/approve-spo-record/<int:record_id>/', views.approve_spo_record_ajax, name='approve_spo_record_ajax'),
    path('ajax/cfa-records/', views.cfa_records_ajax, name='cfa_records_ajax'),
    path('ajax/approve-cfa-record/<int:record_id>/', views.approve_cfa_record_ajax, name='approve_cfa_record_ajax'),
    path('ajax/transporter-records/', views.transporter_records_ajax, name='transporter_records_ajax'),
    path('ajax/approve-transporter-record/<int:record_id>/', views.approve_transporter_record_ajax, name='approve_transporter_record_ajax'),
    
    # Partner Management URLs
    path('spo-rent/<int:spo_id>/add-partner/', views.add_partner, name='add_partner'),
    path('spo-rent/<int:spo_id>/partners-list/', views.spo_partners_list, name='spo_partners_list'),
    path('spo-rent/<int:spo_id>/partners/', views.get_partners, name='get_partners'),
    path('spo-rent/<int:spo_id>/check-partner-limit/', views.check_partner_limit, name='check_partner_limit'),
    path('partner/<int:partner_id>/view/', views.partner_view, name='partner_view'),
    path('partner/<int:partner_id>/edit/', views.partner_edit, name='partner_edit'),
    
    # CFA Partner Management URLs
    path('cfa-agreement/<int:cfa_id>/add-partner/', views.add_cfa_partner, name='add_cfa_partner'),
    path('cfa-agreement/<int:cfa_id>/partners-list/', views.cfa_partners_list, name='cfa_partners_list'),
    path('cfa-agreement/<int:cfa_id>/partners/', views.get_cfa_partners, name='get_cfa_partners'),

    path('cfa-agreement/<int:cfa_id>/check-partner-limit/', views.check_cfa_partner_limit, name='check_cfa_partner_limit'),
    path('cfa-partner/<int:partner_id>/view/', views.cfa_partner_view, name='cfa_partner_view'),
    path('cfa-partner/<int:partner_id>/edit/', views.cfa_partner_edit, name='cfa_partner_edit'),
    
    # Transporter Partner Management URLs
    path('transporter-agreement/<int:transporter_id>/add-partner/', views.add_transporter_partner, name='add_transporter_partner'),
    path('transporter-agreement/<int:transporter_id>/partners-list/', views.transporter_partners_list, name='transporter_partners_list'),
    path('transporter-agreement/<int:transporter_id>/partners/', views.get_transporter_partners, name='get_transporter_partners'),
    path('transporter-agreement/<int:transporter_id>/check-partner-limit/', views.check_transporter_partner_limit, name='check_transporter_partner_limit'),
    path('transporter-partner/<int:partner_id>/view/', views.transporter_partner_view, name='transporter_partner_view'),
    path('transporter-partner/<int:partner_id>/edit/', views.transporter_partner_edit, name='transporter_partner_edit'),
    
    # Chatbot URLs
    path('chatbot/', views.chatbot_management, name='chatbot_management'),
    path('chatbot/questions/', views.chatbot_questions, name='chatbot_questions'),
    path('chatbot/response/<int:question_id>/', views.chatbot_response, name='chatbot_response'),
    path('chatbot/history/', views.chatbot_session_history, name='chatbot_session_history'),
    path('chatbot/question/edit/<int:question_id>/', views.chatbot_question_edit, name='chatbot_question_edit'),
    path('chatbot/question/delete/<int:question_id>/', views.chatbot_question_delete, name='chatbot_question_delete'),

    # User Profile and Settings URLs
    path('profile/', views.user_profile, name='user_profile'),
    path('settings/', views.user_settings, name='user_settings'),

] 