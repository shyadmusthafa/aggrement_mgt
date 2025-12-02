from django.contrib import admin
from .models import IndianState, SPORent, CFAAgreement, TransporterAgreement, Approval, MasState, MasStateBranch, MasConstruction, MasPartner, MasPlant
from .models import ChatbotQuestion, ChatbotSession, ChatbotMessage
from .models import ApprovalWorkflow, ApprovalWorkflowHistory
from .models import UserMenuAccess
from .models import MasDistrict

# Register your models here.
@admin.register(IndianState)
class IndianStateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_union_territory')
    list_filter = ('is_union_territory',)
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(MasState)
class MasStateAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'state_code', 'status')
    list_filter = ('status',)
    search_fields = ('state_name', 'state_code')
    ordering = ('state_name',)

@admin.register(MasStateBranch)
class MasStateBranchAdmin(admin.ModelAdmin):
    list_display = ('state_branch_name', 'state', 'state_branch_code')
    list_filter = ('state',)
    search_fields = ('state_branch_name', 'state_branch_code', 'state__state_name')
    ordering = ('state__state_name', 'state_branch_name')

@admin.register(MasConstruction)
class MasConstructionAdmin(admin.ModelAdmin):
    list_display = ('name', 'remark', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'remark')
    ordering = ('name',)
    list_editable = ('status',)

@admin.register(MasPartner)
class MasPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'remark', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'remark')
    ordering = ('name',)
    list_editable = ('status',)

@admin.register(MasPlant)
class MasPlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('status',)
    search_fields = ('name',)
    ordering = ('name',)
    list_editable = ('status',)

@admin.register(MasDistrict)
class MasDistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'mas_state', 'mas_branch', 'status']
    list_filter = ['status', 'mas_state', 'mas_branch']
    search_fields = ['name', 'code', 'mas_state__name', 'mas_branch__name']
    ordering = ['mas_state__name', 'mas_branch__name', 'name']
    list_editable = ['status']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code')
        }),
        ('Relationships', {
            'fields': ('mas_state', 'mas_branch')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('mas_state', 'mas_branch')

@admin.register(SPORent)
class SPORentAdmin(admin.ModelAdmin):
    list_display = ('spo_name', 'spo_code', 'owner_name', 'state', 'cfa_status', 'status', 'created_at')
    list_filter = ('cfa_status', 'status', 'state', 'created_at')
    search_fields = ('spo_name', 'spo_code', 'owner_name', 'state')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('state', 'branch', 'district_code', 'spo_code', 'spo_name', 'stru_grp', 'cfa_status')
        }),
        ('Agreement Details', {
            'fields': ('inception_date',)
        }),
        ('Owner Information', {
            'fields': ('godown_address', 'owner_name', 'owner_contact_no', 'owner_code', 'owner_address', 'owner_gst', 'gst_status', 'state_code', 'pan_number', 'entity_code', 'declaration_rcm', 'declaration_status', 'owner_pan', 'cfa_mail_id')
        }),
        ('Bank Information', {
            'fields': ('bank_account_name', 'bank_account_no', 'bank_name', 'bank_branch_name', 'bank_ifsc_code')
        }),
        ('Financial Details', {
            'fields': ('destination_code', 'office_sqft', 'open_space_sqft')
        }),
        ('Additional Information', {
            'fields': ('remarks', 'status')
        }),
        ('Documents', {
            'fields': ('transporter_agreement', 'closure_letter', 'closure_acceptance_letter', 'ff_letter_calc', 'security_deposit', 'kyc_document', 'consolidate_document'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )



@admin.register(CFAAgreement)
class CFAAgreementAdmin(admin.ModelAdmin):
    list_display = ('cfa_name', 'cfa_code', 'spo_name', 'state', 'district', 'cfa_status', 'customer_code', 'created_at')
    list_filter = ('cfa_status', 'state', 'district', 'agreement_renewal', 'created_at')
    search_fields = ('cfa_name', 'cfa_code', 'spo_name', 'owner_name', 'state', 'district', 'customer_code')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('state', 'branch', 'district', 'district_code', 'spo_code', 'spo_name', 'stru_grp', 'cfa_status')
        }),
        ('Agreement Details', {
            'fields': ('agreement_renewal', 'inception_date', 'agreement_from_date', 'agreement_to_date')
        }),
        ('CFA Information', {
            'fields': ('godown_address', 'cfa_code', 'cfa_name', 'cfa_address', 'owner_name', 'owner_contact_no', 'cfa_mail_id')
        }),
        ('Business Details', {
            'fields': ('gst_no', 'pan_no')
        }),
        ('Bank Information', {
            'fields': ('bank_account_name', 'bank_account_no', 'bank_name', 'bank_branch_name', 'bank_ifsc_code')
        }),
        ('Financial Details', {
            'fields': ('destination_code', 'security_deposit_rs', 'security_deposit_doc_ref_dd')
        }),
        ('Additional Information', {
            'fields': ('closure_date', 'remarks', 'customer_code')
        }),
        ('Documents', {
            'fields': ('cfa_agreement', 'closure_letter', 'closure_acceptance_letter', 'ff_letter_calc', 'security_deposit', 'kyc_document', 'consolidate_attachment'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(TransporterAgreement)
class TransporterAgreementAdmin(admin.ModelAdmin):
    list_display = ('transporter_name', 'transporter_code', 'source_plant_name', 'state', 'district', 'sale_organization', 'transporter_status', 'status', 'created_at')
    list_filter = ('transporter_status', 'status', 'state', 'district', 'sale_organization', 'operating_in_multiple_plant', 'created_at')
    search_fields = ('transporter_name', 'transporter_code', 'source_plant_name', 'owner_managing_partner', 'state', 'district', 'sale_organization')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('state', 'sale_organization', 'district', 'district_code', 'source_plant_code', 'source_plant_name', 'operating_in_multiple_plant', 'list_of_plant', 'transporter_status')
        }),
        ('Agreement Details', {
            'fields': ('inception_date', 'agreement_from_date', 'agreement_to_date')
        }),
        ('Transporter Information', {
            'fields': ('transporter_code', 'transporter_name', 'transporter_address', 'pincode', 'owner_managing_partner', 'owner_contact_no', 'transporter_mail_id')
        }),
        ('Business Details', {
            'fields': ('gst_no', 'pan_no', 'gst_status', 'state_code', 'pan_number', 'entity_code', 'declaration_rcm', 'declaration_status')
        }),
        ('Bank Information', {
            'fields': ('bank_account_name', 'bank_account_no', 'bank_name', 'branch_name', 'bank_ifsc_code')
        }),
        ('Financial Details', {
            'fields': ('customer_code_for_invoicing', 'security_deposit_rs', 'security_deposit_doc_dd')
        }),
        ('Additional Information', {
            'fields': ('reg_office_destination_code', 'closure_date', 'remark', 'status')
        }),
        ('Documents', {
            'fields': ('transporter_agreement', 'closure_letter', 'closure_acceptance_letter', 'ff_letter_calc', 'security_deposit', 'kyc_document'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('nfa_no', 'name', 'nature_of_approval', 'status', 'valid_from', 'valid_to', 'created_at')
    list_filter = ('status', 'nature_of_approval', 'created_at', 'valid_from', 'valid_to')
    search_fields = ('nfa_no', 'name', 'code', 'subject')
    readonly_fields = ('created_at', 'updated_at', 'approved_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('nfa_no', 'nfa_date', 'nature_of_approval', 'code', 'name', 'subject')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Status & Remarks', {
            'fields': ('status', 'remark')
        }),
        ('Metadata', {
            'fields': ('created_by', 'approved_by', 'approved_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new approval
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ApprovalWorkflow)
class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = ['record_type', 'record_code', 'status', 'submitted_by', 'submitted_at', 'approved_by', 'approved_at']
    list_filter = ['status', 'record_type', 'submitted_at', 'approved_at']
    search_fields = ['record_code', 'approver_remarks']
    readonly_fields = ['created_at', 'submitted_at', 'approved_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Record Information', {
            'fields': ('record_type', 'record_id', 'record_code')
        }),
        ('Approval Information', {
            'fields': ('status', 'approver_remarks')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'submitted_at', 'approved_at'),
            'classes': ('collapse',)
        }),
        ('User Information', {
            'fields': ('submitted_by', 'approved_by')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('submitted_by', 'approved_by')


@admin.register(ApprovalWorkflowHistory)
class ApprovalWorkflowHistoryAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'action', 'user', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['workflow__record_code', 'remarks']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Workflow Information', {
            'fields': ('workflow', 'action')
        }),
        ('User Information', {
            'fields': ('user', 'remarks')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('workflow', 'user')


@admin.register(ChatbotQuestion)
class ChatbotQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'response']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'question']
    
    fieldsets = (
        ('Question Details', {
            'fields': ('question', 'response', 'category')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ChatbotSession)
class ChatbotSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'started_at', 'last_activity', 'is_active']
    list_filter = ['is_active', 'started_at', 'last_activity']
    search_fields = ['session_id', 'user__username']
    readonly_fields = ['session_id', 'started_at', 'last_activity']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(ChatbotMessage)
class ChatbotMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content', 'session__session_id']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session', 'question')

# Simple User Menu Control Admin
@admin.register(UserMenuAccess)
class UserMenuAccessAdmin(admin.ModelAdmin):
    """Admin for User Menu Access"""
    list_display = ['user', 'spo_menu_enabled', 'cfa_menu_enabled', 'transport_menu_enabled', 'approval_menu_enabled', 'approval_workflow_enabled', 'report_enabled', 'mail_reminder_enabled', 'user_management_enabled', 'user_menu_access_control_enabled', 'updated_at']
    list_filter = ['spo_menu_enabled', 'cfa_menu_enabled', 'transport_menu_enabled', 'approval_menu_enabled', 'approval_workflow_enabled', 'report_enabled', 'mail_reminder_enabled', 'user_management_enabled', 'user_menu_access_control_enabled']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Main Menu Access Control', {
            'fields': ('spo_menu_enabled', 'cfa_menu_enabled', 'transport_menu_enabled', 'approval_menu_enabled')
        }),
        ('Additional Menu Access Control', {
            'fields': ('approval_workflow_enabled', 'report_enabled', 'mail_reminder_enabled', 'user_management_enabled', 'user_menu_access_control_enabled')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


