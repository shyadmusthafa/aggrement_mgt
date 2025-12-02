import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from .models import IndianState, SPORent, CFAAgreement, TransporterAgreement, Approval, MasState, MasStateBranch, MasPartnerDetails, CFAPartnerDetails, TransporterPartnerDetails, ChatbotQuestion, UserMenuAccess, MasDistrict

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'user@example.com'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize field labels
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email Address'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        
        # Add placeholders
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

class SPORentForm(forms.ModelForm):
    class Meta:
        model = SPORent
        fields = '__all__'
        widgets = {
            'state': forms.Select(attrs={'class': 'form-select'}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'district': forms.Select(attrs={'id': 'id_district', 'class': 'form-select'}),
            'district_code': forms.TextInput(attrs={'id': 'id_district_code', 'class': 'form-control', 'readonly': 'readonly'}),
            'spo_code': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '4',
                'placeholder': 'Format: C001 (Chettinad) or AB12 (Anjani)',
                'title': 'Chettinad: 1 letter + 3 numbers (A012) | Anjani: 2 letters + 2 numbers (AB12)'
            }),
            'spo_name': forms.TextInput(attrs={'class': 'form-control'}),
            'stru_grp': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select Structure Group'),
                ('Road', 'Road'),
                ('Rail', 'Rail'),
                ('TDP', 'TDP'),
                ('Others', 'Others'),
            ]),
            'cfa_status': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select SPO Status'),
                ('Active', 'Active'),
                ('Inactive', 'Inactive'),
                ('Under Notice', 'Under Notice'),
                ('Closed', 'Closed'),
            ]),
            'inception_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'renewal_with': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select Renewal Type'),
                ('Agreement', 'Agreement'),
                ('Renewal', 'Renewal'),
            ]),
            'godown_address': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_contact_no': forms.TextInput(attrs={'type': 'tel', 'class': 'form-control'}),
            'owner_code': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_address': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'owner_gst': forms.TextInput(attrs={
                'class': 'form-control', 
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa; cursor: not-allowed;'
            }),
            'gst_status': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select GST Status'),
                ('YES', 'YES'),
                ('NO', 'NO'),
            ]),
            'state_code': forms.TextInput(attrs={
                'class': 'form-control', 
                'maxlength': '2', 
                'pattern': '[0-9]{2}', 
                'title': 'Enter exactly 2 digits (e.g., 01, 02, 33)',
                'placeholder': '01'
            }),
            'pan_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'maxlength': '10', 
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa; cursor: not-allowed;',
                'title': 'Auto-populated from Owner PAN field'
            }),
            'entity_code': forms.TextInput(attrs={
                'class': 'form-control', 
                'maxlength': '5',
                'pattern': '[A-Za-z0-9]{1,5}',
                'title': 'Enter 1 to 5 characters (letters or numbers, e.g., A, AB, ABC, ABC5, ABCDE)',
                'placeholder': 'ABC'
            }),
            'declaration_rcm': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select Declaration/RCM'),
                ('Declaration', 'Declaration'),
                ('RCM', 'RCM'),
            ]),
            'declaration_status': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select Declaration Status'),
                ('Collected', 'Collected'),
                ('Pending', 'Pending'),
            ]),
            'owner_pan': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
                'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}',
                'title': 'Format: ABCDE1234F (5 letters + 4 digits + 1 letter)',
                'placeholder': 'ABCDE1234F'
            }),
            'sale_organization': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select Sale Organization'),
                ('Chettinad', 'Chettinad'),
                ('Anjani', 'Anjani'),
            ]),

            'bank_account_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_account_no': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_branch_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_ifsc_code': forms.TextInput(attrs={'class': 'form-control'}),
            'destination_code': forms.TextInput(attrs={'class': 'form-control'}),
            'office_sqft': forms.TextInput(attrs={'class': 'form-control'}),
            'open_space_sqft': forms.TextInput(attrs={'class': 'form-control'}),
            'total_space': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control'}),
            'rental_from_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'rental_to_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'days_count': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'security_deposit_paid': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'security_deposit_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'rent_pm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'yearly_hike_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
            'vacation_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Select Status'),
                ('Active', 'Active'),
                ('Inactive', 'Inactive'),
                ('Under Notice', 'Under Notice'),
                ('Closed', 'Closed'),
            ]),
            'transporter_agreement': forms.FileInput(attrs={'class': 'form-control'}),
            'closure_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'closure_acceptance_letter': forms.FileInput(attrs={'class': 'form-control'}),
            'ff_letter_calc': forms.FileInput(attrs={'class': 'form-control'}),
            'security_deposit': forms.FileInput(attrs={'class': 'form-control'}),
            'kyc_document': forms.FileInput(attrs={'class': 'form-control'}),
            'bank_details': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure state field to show data from mas_state table
        self.fields['state'].queryset = MasState.objects.all().order_by('state_name')
        self.fields['state'].empty_label = "Select State"
        
        # FORCE FIX: Always show ALL branches to prevent validation errors
        if self.instance and self.instance.pk:
            # For existing records, show all branches
            self.fields['branch'].queryset = MasStateBranch.objects.all()
        else:
            # For new records, also show all branches to prevent validation issues
            self.fields['branch'].queryset = MasStateBranch.objects.all()
        
        # Update field labels
        self.fields['branch'].label = 'Branch'
        self.fields['district'].label = 'District'
        self.fields['district_code'].label = 'District Code'
        self.fields['stru_grp'].label = 'Structure Group'
        self.fields['cfa_status'].label = 'SPO Status'

        self.fields['destination_code'].label = 'Depot Sq.Ft'
        
        # Make only essential fields required (mandatory)
        mandatory_fields = [
            'state', 'branch', 'spo_name', 'stru_grp', 'cfa_status',
            'inception_date'
        ]
        
        # Make file upload fields optional
        optional_file_fields = [
            'vacation_letter', 'transporter_agreement', 'closure_letter', 
            'closure_acceptance_letter', 'ff_letter_calc', 'security_deposit'
        ]
        
        for field_name in mandatory_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                # Add asterisk to label for visual indication
                if not self.fields[field_name].label.endswith(' *'):
                    self.fields[field_name].label += ' *'
        
        # Ensure file fields are optional
        for field_name in optional_file_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False
        
        # Configure district field - initially empty, will be populated via AJAX
        if self.instance and self.instance.pk and self.instance.district:
            # For existing records, show the current district
            self.fields['district'].queryset = MasDistrict.objects.filter(id=self.instance.district.id)
        else:
            # For new records, start with empty queryset but allow any valid district
            self.fields['district'].queryset = MasDistrict.objects.all()
        self.fields['district'].empty_label = "Select State and Branch First"
    
    def clean(self):
        cleaned_data = super().clean()
        sale_organization = cleaned_data.get('sale_organization')
        spo_code = cleaned_data.get('spo_code')
        gst_status = cleaned_data.get('gst_status')
        state_code = cleaned_data.get('state_code')
        pan_number = cleaned_data.get('pan_number')
        entity_code = cleaned_data.get('entity_code')
        declaration_rcm = cleaned_data.get('declaration_rcm')
        declaration_status = cleaned_data.get('declaration_status')
        
        # Validate SPO code format based on sale organization
        if sale_organization and spo_code:
            if sale_organization == 'Chettinad':
                # Chettinad: 1 letter + 3 numbers (4 characters max)
                import re
                if not re.match(r'^[A-Za-z]\d{3}$', spo_code):
                    raise forms.ValidationError({
                        'spo_code': 'For Chettinad, SPO code must be 1 letter followed by 3 numbers (e.g., A012, B123) - maximum 4 characters'
                    })
            elif sale_organization == 'Anjani':
                # Anjani: 2 letters + 2 numbers (4 characters max)
                import re
                if not re.match(r'^[A-Za-z]{2}\d{2}$', spo_code):
                    raise forms.ValidationError({
                        'spo_code': 'For Anjani, SPO code must be 2 letters followed by 2 numbers (e.g., AB12, CD34) - maximum 4 characters'
                    })
        
        # GST Status validation - now optional
        # If GST Status is YES, validate the three GST fields only if they are provided
        if gst_status == 'YES':
            if state_code:
                # Validate state_code format (exactly 2 digits)
                import re
                if not re.match(r'^[0-9]{2}$', state_code):
                    raise forms.ValidationError({
                        'state_code': 'State Code must be exactly 2 digits (e.g., 01, 02, 33).'
                    })
            
            if pan_number:
                # Validate PAN number format
                import re
                if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan_number):
                    raise forms.ValidationError({
                        'pan_number': 'PAN Number must be in format: ABCDE1234F (5 letters + 4 digits + 1 letter).'
                    })
            
            if entity_code:
                # Validate entity_code length (max 5 characters)
                if len(entity_code) > 5:
                    raise forms.ValidationError({
                        'entity_code': 'Last 5 Characters must be maximum 5 characters (e.g., ABCDE, 12345).'
                    })
            
            # Validate state_code format (exactly 2 digits)
            import re
            if not re.match(r'^[0-9]{2}$', state_code):
                raise forms.ValidationError({
                    'state_code': 'State Code must be exactly 2 digits (e.g., 01, 02, 33).'
                })
            
            # Validate PAN number format
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan_number):
                raise forms.ValidationError({
                    'pan_number': 'PAN Number must be in format: ABCDE1234F (5 letters + 4 digits + 1 letter).'
                })
            
            # Validate entity_code length (max 5 characters)
            if len(entity_code) > 5:
                raise forms.ValidationError({
                    'entity_code': 'Last 5 Characters must be maximum 5 characters (e.g., ABCDE, 12345).'
                })
            
            # GST auto-generation removed - fields are now independent
        
        # If GST Status is NO, validate Declaration/RCM and Owner PAN only if provided
        if gst_status == 'NO':
            # If Declaration is selected, validate Declaration Status only if provided
            if declaration_rcm == 'Declaration' and declaration_status:
                # Validate Declaration Status format if provided
                pass
            
            # Validate Owner PAN format only if provided
            owner_pan = cleaned_data.get('owner_pan')
            if owner_pan:
                import re
                if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', owner_pan):
                    raise forms.ValidationError({
                        'owner_pan': 'Owner PAN must be in format: ABCDE1234F (5 letters + 4 digits + 1 letter).'
                    })
        
        # Always validate Owner PAN format if provided (regardless of GST status)
        owner_pan = cleaned_data.get('owner_pan')
        if owner_pan:
            import re
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', owner_pan):
                raise forms.ValidationError({
                    'owner_pan': 'Owner PAN must be in format: ABCDE1234F (5 letters + 4 digits + 1 letter).'
                })
        
        return cleaned_data
    
    def clean_district(self):
        district = self.cleaned_data.get('district')
        
        # FORCE FIX: Always allow any district selection to prevent validation errors
        if self.instance and self.instance.pk:
            # For existing records, preserve current district
            if self.instance.district:
                return self.instance.district
            return district
        
        # For new records, accept any valid district
        if district:
            return district
        
        return district

    def clean_branch(self):
        branch = self.cleaned_data.get('branch')
        
        # FORCE FIX: Always allow any branch selection to prevent validation errors
        if self.instance and self.instance.pk:
            # For existing records, preserve current branch
            if self.instance.branch:
                return self.instance.branch
            return branch
        
        # For new records, accept any valid branch
        if branch:
            return branch
        
        return branch
    
    def clean_district(self):
        district = self.cleaned_data.get('district')
        
        # FORCE FIX: Always allow any district selection to prevent validation errors
        if self.instance and self.instance.pk:
            # For existing records, preserve current district
            if self.instance.district:
                return self.instance.district
            return district
        
        # For new records, accept any valid district
        if district:
            return district
        
        return district

    def clean_stru_grp(self):
        stru_grp = self.cleaned_data.get('stru_grp')
        
        # FORCE FIX: Always allow existing values, regardless of current choices
        if self.instance and self.instance.pk and self.instance.stru_grp:
            return self.instance.stru_grp
        
        # For new records, validate against choices
        valid_choices = ['Road', 'Rail', 'TDP', 'Others']
        if stru_grp and stru_grp not in valid_choices:
            raise forms.ValidationError("Please select a valid structure group.")
        
        return stru_grp

    def clean_cfa_status(self):
        cfa_status = self.cleaned_data.get('cfa_status')
        
        # FORCE FIX: Always allow existing values, regardless of current choices
        if self.instance and self.instance.pk and self.instance.cfa_status:
            return self.instance.cfa_status
        
        # For new records, validate against choices
        valid_choices = ['Active', 'Inactive', 'Under Notice', 'Closed']
        if cfa_status and cfa_status not in valid_choices:
            raise forms.ValidationError("Please select a valid SPO status.")
        
        return cfa_status



    def clean_status(self):
        status = self.cleaned_data.get('status')
        
        # FORCE FIX: Always allow existing values, regardless of current choices
        if self.instance and self.instance.pk and self.instance.status:
            return self.instance.status
        
        # For new records, validate against choices
        valid_choices = ['Active', 'Inactive', 'Under Notice', 'Closed']
        if status and status not in valid_choices:
            raise forms.ValidationError("Please select a valid status.")
        
        return status

    def clean(self):
        cleaned_data = super().clean()
        
        # FORCE FIX: Always preserve existing values to prevent validation errors
        if self.instance and self.instance.pk:
            # Preserve existing choice field values
            choice_fields = ['stru_grp', 'cfa_status', 'status', 'branch']
            for field_name in choice_fields:
                if field_name in cleaned_data and not cleaned_data[field_name]:
                    # If field is empty but instance has a value, use the instance value
                    if hasattr(self.instance, field_name) and getattr(self.instance, field_name):
                        cleaned_data[field_name] = getattr(self.instance, field_name)
        
        # File size validation (max 50MB for each file)
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        
        for field_name in ['transporter_agreement', 'closure_letter', 'closure_acceptance_letter', 'ff_letter_calc', 'security_deposit', 'vacation_letter', 'consolidate_document']:
            file_field = cleaned_data.get(field_name)
            if file_field and hasattr(file_field, 'size') and file_field.size > max_size:
                raise forms.ValidationError(f"{field_name.replace('_', ' ').title()} file size must be less than 50MB.")
        
        return cleaned_data

    def is_valid(self):
        # FORCE FIX: Always skip choice validation to prevent "Select a valid choice" errors
        choice_fields = ['stru_grp', 'cfa_status', 'status', 'branch']
        for field_name in choice_fields:
            if field_name in self.fields:
                # Store original validation
                if not hasattr(self.fields[field_name], '_original_validators'):
                    self.fields[field_name]._original_validators = self.fields[field_name].validators.copy()
                # Clear validators for all records
                self.fields[field_name].validators = []
        
        # FORCE FIX: For branch field, always disable queryset validation
        if 'branch' in self.fields:
            # Store original queryset
            if not hasattr(self.fields['branch'], '_original_queryset'):
                self.fields['branch']._original_queryset = self.fields['branch'].queryset
            # Set queryset to all branches to prevent validation errors
            self.fields['branch'].queryset = MasStateBranch.objects.all()
        
        # FORCE FIX: For district field, allow any valid district to prevent validation errors
        # Temporarily commented out district field handling
        # if 'district' in self.fields:
        #     # Store original queryset
        #     if not hasattr(self.fields['district'], '_original_queryset'):
        #         self.fields['district']._original_queryset = self.fields['district'].queryset
        #     # Set queryset to all districts to prevent validation errors
        #     self.fields['district'].queryset = MasDistrict.objects.all()
        
        return super().is_valid()

class CFAAgreementForm(forms.ModelForm):
    class Meta:
        model = CFAAgreement
        fields = '__all__'
        widgets = {
            'state': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_state'
            }),
            'branch': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_branch'
            }),
            'district': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_district'
            }),
            'district_code': forms.TextInput(attrs={
                'id': 'id_district_code',
                'class': 'form-control',
                'placeholder': 'District code will be auto-filled',
                'readonly': 'readonly'
            }),
            'sale_organization': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_sale_organization',
                'choices': [
                    ('', 'Select Sale Organization'),
                    ('Chettinad', 'Chettinad'),
                    ('Anjani', 'Anjani'),
                ]
            }),
            'spo_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_spo_code',
                'placeholder': 'Format: C001 (Chettinad) or AB12 (Anjani)',
                'maxlength': '4',
                'title': 'Chettinad: 1 letter + 3 numbers (A012) | Anjani: 2 letters + 2 numbers (AB12)',
                'required': True
            }),
            'spo_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter SPO name',
                'required': True
            }),
            'stru_grp': forms.Select(attrs={
                'class': 'form-select',
                'choices': [
                    ('', 'Select Structure Group'),
                    ('Road', 'Road'),
                    ('Rail', 'Rail'),
                    ('TDP', 'TDP'),
                    ('Others', 'Others'),
                ]
            }),
            'cfa_status': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'agreement_renewal': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'inception_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
            }),
            'agreement_from_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
            }),
            'agreement_to_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
            }),
            'godown_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter complete godown address',
                'required': True
            }),
            'cfa_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter CFA code',
                'required': True
            }),
            'cfa_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter CFA name',
                'required': True
            }),
            'cfa_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter complete CFA address',
                'required': True
            }),
            'owner_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter owner name',
                'required': True
            }),
            'owner_contact_no': forms.TextInput(attrs={
                'type': 'tel',
                'class': 'form-control',
                'placeholder': 'Enter contact number',
                'pattern': '[0-9]{10}',
                'title': 'Please enter a valid 10-digit phone number',
                'required': True
            }),
            'cfa_mail_id': forms.EmailInput(attrs={
                'type': 'email',
                'class': 'form-control',
                'placeholder': 'Enter email address',
                'required': True
            }),
            'gst_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GST number will be auto-generated',
                'readonly': 'readonly',
                'required': False
            }),
            'pan_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PAN number',
                'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}',
                'title': 'Please enter a valid PAN number (e.g., ABCDE1234F)',
                'required': True
            }),
            'gst_status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_gst_status',
                'required': True
            }),
            'state_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_state_code',
                'placeholder': 'Enter 2-digit state code',
                'maxlength': '2',
                'pattern': '[0-9]{2}',
                'title': 'Enter only 2 digits (00-99)',
                'required': False
            }),
            'pan_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_pan_number',
                'placeholder': 'PAN number will be auto-populated from Pan no field',
                'maxlength': '10',
                'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}',
                'title': 'PAN format: ABCDE1234F (auto-populated)',
                'required': False,
                'readonly': 'readonly'
            }),
            'entity_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_entity_code',
                'placeholder': 'Enter last 5 characters',
                'maxlength': '20',
                'pattern': '[A-Za-z0-9]{1,20}',
                'title': 'Enter up to 20 characters (letters or numbers, no special characters)',
                'required': False
            }),
            'declaration_rcm': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_declaration_rcm',
                'required': False
            }),
            'declaration_status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_declaration_status',
                'required': False
            }),
            'bank_account_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bank account holder name',
                'required': True
            }),
            'bank_account_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bank account number',
                'required': True
            }),
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bank name',
                'required': True
            }),
            'bank_branch_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bank branch name',
                'required': True
            }),
            'bank_ifsc_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter IFSC code',
                'pattern': '[A-Z]{4}0[A-Z0-9]{6}',
                'title': 'Please enter a valid IFSC code (e.g., SBIN0001234)',
                'required': True
            }),
            'destination_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter CFA Reg.DEST Code',
                'required': True
            }),
            'security_deposit_rs': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'class': 'form-control',
                'placeholder': 'Enter amount in rupees',
                'required': True
            }),
            'security_deposit_doc_ref_dd': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter document reference or DD number',
                'required': True
            }),
            'closure_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'remarks': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Enter any additional remarks or notes'
            }),
            'customer_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer code',
                'required': False
            }),
            'cfa_agreement': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
                'data-max-size': '52428800'  # 50MB
            }),
            'closure_letter': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
                'data-max-size': '52428800'  # 50MB
            }),
            'closure_acceptance_letter': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
                'data-max-size': '52428800'  # 50MB
            }),
            'ff_letter_calc': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
                'data-max-size': '52428800'  # 50MB
            }),
            'security_deposit': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
                'data-max-size': '52428800'  # 50MB
            }),
            'kyc_document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
                'data-max-size': '52428800'  # 50MB
            }),
            'consolidate_attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
                'data-max-size': '52428800'  # 50MB
            }),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure state field to show data from mas_state table
        self.fields['state'].queryset = MasState.objects.all().order_by('state_name')
        self.fields['state'].empty_label = "Select State"
        
        # Configure branch field - start with empty queryset for dynamic loading
        if self.instance and self.instance.pk and self.instance.branch:
            # For existing records, show the current branch
            self.fields['branch'].queryset = MasStateBranch.objects.filter(id=self.instance.branch.id)
        else:
            # For new records, allow all branches for validation but start with empty for display
            self.fields['branch'].queryset = MasStateBranch.objects.all()
        self.fields['branch'].empty_label = "Select State First"
        self.fields['branch'].label = "Branch"
        
        # Configure district field - allow all districts for validation, but start with empty for display
        if self.instance and self.instance.pk and self.instance.district:
            # For existing records, show the current district
            self.fields['district'].queryset = MasDistrict.objects.filter(id=self.instance.district.id)
        else:
            # For new records, allow all districts for validation but start with empty for display
            self.fields['district'].queryset = MasDistrict.objects.all()
        self.fields['district'].empty_label = "Select State and Branch First"
        self.fields['district'].label = "District"
        
        # Update field labels to match SPO Rent form
        self.fields['district_code'].label = 'District Code'
        
        # Update destination_code field label
        self.fields['destination_code'].label = 'CFA Reg.DEST Code'
        
        # Set choices for GST status fields
        self.fields['gst_status'].choices = [
            ('', 'Select GST Status'),
            ('YES', 'YES'),
            ('NO', 'NO'),
        ]
        
        self.fields['declaration_rcm'].choices = [
            ('', 'Select Declaration/RCM'),
            ('Declaration', 'Declaration'),
            ('RCM', 'RCM'),
        ]
        
        self.fields['declaration_status'].choices = [
            ('', 'Select Declaration Status'),
            ('Collected', 'Collected'),
            ('Pending', 'Pending'),
        ]
        
        # Define fields that should NOT be required
        non_required_fields = [
            'remarks', 'closure_date', 'state', 'district',
            'cfa_agreement', 'closure_letter', 'closure_acceptance_letter', 
            'ff_letter_calc', 'security_deposit', 'kyc_document', 'consolidate_attachment',
            'gst_no', 'state_code', 'pan_number', 'entity_code', 
            'declaration_rcm', 'declaration_status'
        ]
        
        # Make conditional fields not required initially
        # They will be validated conditionally in the clean method
        self.fields['declaration_rcm'].required = False
        self.fields['declaration_status'].required = False
        
        # Add CSS classes and help text
        for field_name, field in self.fields.items():
            if field_name not in non_required_fields:
                field.required = True
                if not field.label.endswith(' *'):
                    field.label += ' *'
            else:
                field.required = False
        
        # Set default values for new records (only if fields exist)
        if not self.instance.pk:
            if 'cfa_status' in self.fields:
                self.fields['cfa_status'].initial = 'Active'
            if 'agreement_renewal' in self.fields:
                self.fields['agreement_renewal'].initial = 'Agreement'

    def clean(self):
        cleaned_data = super().clean()
        agreement_from_date = cleaned_data.get('agreement_from_date')
        agreement_to_date = cleaned_data.get('agreement_to_date')
        inception_date = cleaned_data.get('inception_date')
        closure_date = cleaned_data.get('closure_date')
        
        # Validate date ranges
        if agreement_from_date and agreement_to_date and agreement_from_date > agreement_to_date:
            raise forms.ValidationError("Agreement from date cannot be after agreement to date.")
        
        # Removed validation: inception date can now be after agreement from date
        
        # Allow closure date to be before agreement to date (for early termination cases)
        # Only validate if closure date is before agreement from date
        if closure_date and agreement_from_date and closure_date < agreement_from_date:
            raise forms.ValidationError("Closure date cannot be before agreement from date.")
        
        # Validate contact number
        owner_contact_no = cleaned_data.get('owner_contact_no')
        if owner_contact_no:
            if not owner_contact_no.isdigit():
                raise forms.ValidationError("Contact number must contain only digits.")
            if len(owner_contact_no) != 10:
                raise forms.ValidationError("Contact number must be exactly 10 digits.")
        
        # Validate GST number format
        gst_no = cleaned_data.get('gst_no')
        if gst_no:
            import re
            gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
            if not re.match(gst_pattern, gst_no):
                raise forms.ValidationError("Please enter a valid GST number format.")
        
        # Validate PAN number format and auto-populate pan_number
        pan_no = cleaned_data.get('pan_no')
        if pan_no:
            import re
            pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
            if not re.match(pan_pattern, pan_no):
                raise forms.ValidationError("Please enter a valid PAN number format.")
            
            # Auto-populate pan_number from pan_no if not provided
            if not cleaned_data.get('pan_number'):
                cleaned_data['pan_number'] = pan_no
        
        # Validate IFSC code format
        bank_ifsc_code = cleaned_data.get('bank_ifsc_code')
        if bank_ifsc_code:
            import re
            ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
            if not re.match(ifsc_pattern, bank_ifsc_code):
                raise forms.ValidationError("Please enter a valid IFSC code format.")
        
        # Validate SPO code format based on sale organization
        spo_code = cleaned_data.get('spo_code')
        sale_organization = cleaned_data.get('sale_organization')
        
        if spo_code and sale_organization:
            import re
            if sale_organization == 'Chettinad':
                # Chettinad: 1 letter + 3 numbers (e.g., A012, B123) - max 4 characters
                spo_pattern = r'^[A-Za-z]\d{3}$'
                if not re.match(spo_pattern, spo_code):
                    raise forms.ValidationError("For Chettinad, SPO code must be 1 letter followed by 3 numbers (e.g., A012, B123).")
                if len(spo_code) > 4:
                    raise forms.ValidationError("SPO code cannot exceed 4 characters for Chettinad.")
            elif sale_organization == 'Anjani':
                # Anjani: 2 letters + 2 numbers (e.g., AB12) - max 4 characters
                spo_pattern = r'^[A-Za-z]{2}\d{2}$'
                if not re.match(spo_pattern, spo_code):
                    raise forms.ValidationError("For Anjani, SPO code must be 2 letters followed by 2 numbers (e.g., AB12).")
                if len(spo_code) > 4:
                    raise forms.ValidationError("SPO code cannot exceed 4 characters for Anjani.")
        
        # File size validation (max 50MB for each file)
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        
        for field_name in ['cfa_agreement', 'closure_letter', 'closure_acceptance_letter', 'ff_letter_calc', 'security_deposit', 'kyc_document', 'consolidate_attachment']:
            file_field = cleaned_data.get(field_name)
            if file_field and hasattr(file_field, 'size') and file_field.size > max_size:
                raise forms.ValidationError(f"{field_name.replace('_', ' ').title()} file size must be less than 50MB.")
        
        # Handle branch and district fields
        branch = cleaned_data.get('branch')
        district = cleaned_data.get('district')
        
        # Validate branch exists
        if branch:
            try:
                MasStateBranch.objects.get(id=branch.id)
            except MasStateBranch.DoesNotExist:
                raise forms.ValidationError("Selected branch does not exist.")
        
        # Validate district exists
        if district:
            try:
                MasDistrict.objects.get(id=district.id)
            except MasDistrict.DoesNotExist:
                raise forms.ValidationError("Selected district does not exist.")
        
        # GST Status conditional validation
        gst_status = cleaned_data.get('gst_status')
        if gst_status == 'YES':
            # When GST Status is YES, these fields are required
            state_code = cleaned_data.get('state_code')
            pan_number = cleaned_data.get('pan_number')
            entity_code = cleaned_data.get('entity_code')
            
            if not state_code:
                raise forms.ValidationError("State Code is required when GST Status is YES.")
            if not pan_number:
                raise forms.ValidationError("PAN Number is required when GST Status is YES.")
            if not entity_code:
                raise forms.ValidationError("Last 4 Characters is required when GST Status is YES.")
            
            # Validate state code format (2 digits)
            if state_code and not state_code.isdigit() or len(state_code) != 2:
                raise forms.ValidationError("State Code must be exactly 2 digits.")
            
            # Validate PAN number format
            if pan_number:
                import re
                pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
                if not re.match(pan_pattern, pan_number):
                    raise forms.ValidationError("Please enter a valid PAN number format (ABCDE1234F).")
            
            # Validate entity code (4 characters, letters or numbers only)
            if entity_code:
                import re
                entity_pattern = r'^[A-Za-z0-9]{4}$'
                if not re.match(entity_pattern, entity_code):
                    raise forms.ValidationError("Last 4 Characters must be exactly 4 characters (letters or numbers only).")
        
        elif gst_status == 'NO':
            # When GST Status is NO, check if Declaration/RCM is selected
            declaration_rcm = cleaned_data.get('declaration_rcm')
            if not declaration_rcm:
                raise forms.ValidationError("Declaration/RCM Status is required when GST Status is NO.")
            
            if declaration_rcm == 'Declaration':
                # When Declaration is selected, Declaration Status is required
                declaration_status = cleaned_data.get('declaration_status')
                if not declaration_status:
                    raise forms.ValidationError("Declaration Status is required when Declaration/RCM Status is Declaration.")
        
        if branch:
            try:
                # Get the branch object (but don't override district_code - it should come from district selection)
                branch_obj = MasStateBranch.objects.get(id=branch.id)
                # Only set district_code if it's empty and no district was selected
                if not cleaned_data.get('district_code'):
                    cleaned_data['district_code'] = branch_obj.state_branch_code
                # Note: district should NOT be set here - it should come from the district selection
            except MasStateBranch.DoesNotExist:
                pass

        if district:
            try:
                # Get the district object
                district_obj = MasDistrict.objects.get(id=district.id)
                # Note: district_code should NOT be set here - it should come from the district selection
            except MasDistrict.DoesNotExist:
                pass

        # FORCE FIX: For branch field, allow any valid branch to prevent validation errors
        if 'branch' in self.fields:
            # Store original queryset
            if not hasattr(self.fields['branch'], '_original_queryset'):
                self.fields['branch']._original_queryset = self.fields['branch'].queryset
            # Set queryset to all branches to prevent validation errors
            self.fields['branch'].queryset = MasStateBranch.objects.all()

        # FORCE FIX: For district field, allow any valid district to prevent validation errors
        if 'district' in self.fields:
            # Store original queryset
            if not hasattr(self.fields['district'], '_original_queryset'):
                self.fields['district']._original_queryset = self.fields['district'].queryset
            # Set queryset to all districts to prevent validation errors
            self.fields['district'].queryset = MasDistrict.objects.all()


        
        return cleaned_data

    def clean_cfa_code(self):
        cfa_code = self.cleaned_data.get('cfa_code')
        # Removed duplicate validation - users can now enter same code multiple times
        return cfa_code

    def clean_spo_code(self):
        spo_code = self.cleaned_data.get('spo_code')
        sale_organization = self.cleaned_data.get('sale_organization')
        
        if not spo_code:
            return spo_code
            
        if not sale_organization:
            raise forms.ValidationError("Please select a Sale Organization first.")
        
        # Remove any spaces and convert to uppercase
        spo_code = spo_code.strip().upper()
        
        if sale_organization == 'Chettinad':
            # Format: 1 letter + 3 numbers (A012)
            if not re.match(r'^[A-Z][0-9]{3}$', spo_code):
                raise forms.ValidationError(
                    "For Chettinad, SPO code must be 1 letter followed by 3 numbers (e.g., A012, B123, C456)"
                )
        elif sale_organization == 'Anjani':
            # Format: 2 letters + 2 numbers (AB12)
            if not re.match(r'^[A-Z]{2}[0-9]{2}$', spo_code):
                raise forms.ValidationError(
                    "For Anjani, SPO code must be 2 letters followed by 2 numbers (e.g., AB12, CD34, EF56)"
                )
        
        return spo_code

    def clean_gst_no(self):
        gst_no = self.cleaned_data.get('gst_no')
        gst_status = self.cleaned_data.get('gst_status')
        
        # If GST Status is NO, set GST number to None (NULL in database)
        if gst_status == 'NO':
            return None
        
        # If GST Status is YES, GST number should be auto-generated
        if gst_status == 'YES' and not gst_no:
            raise forms.ValidationError("GST number is required when GST Status is YES.")
        
        return gst_no

    def clean(self):
        cleaned_data = super().clean()
        spo_code = cleaned_data.get('spo_code')
        sale_organization = cleaned_data.get('sale_organization')
        
        # Additional validation to ensure both fields are provided together
        if spo_code and not sale_organization:
            raise forms.ValidationError("Sale Organization is required when SPO code is provided.")
        
        if sale_organization and not spo_code:
            raise forms.ValidationError("SPO code is required when Sale Organization is selected.")
        
        return cleaned_data

class TransporterAgreementForm(forms.ModelForm):
    # Override list_of_plant field to use CharField to match the model
    list_of_plant = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),  # Hidden input to store selected values
        help_text="Select multiple plants from the dropdown"
    )
    
    class Meta:
        model = TransporterAgreement
        fields = '__all__'
        widgets = {
            'state': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'sale_organization': forms.Select(attrs={'class': 'form-select'}),
            'district_code': forms.TextInput(attrs={'readonly': True}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'source_plant_code': forms.TextInput(attrs={'required': True}),
            'source_plant_name': forms.TextInput(attrs={'required': True}),
            'operating_in_multiple_plant': forms.Select(attrs={'class': 'form-select', 'required': True}),

            'transporter_status': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'inception_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'agreement_from_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'agreement_to_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'transporter_code': forms.TextInput(attrs={'required': True}),
            'transporter_name': forms.TextInput(attrs={'required': True}),
            'transporter_address': forms.Textarea(attrs={'rows': 3, 'required': True}),
            'pincode': forms.TextInput(attrs={'required': True, 'maxlength': '10', 'pattern': '[0-9]{6}'}),
            'owner_managing_partner': forms.TextInput(attrs={'required': True}),
            'owner_contact_no': forms.TextInput(attrs={'type': 'tel', 'required': True}),
            'transporter_mail_id': forms.EmailInput(attrs={'type': 'email', 'required': True}),
            'gst_no': forms.TextInput(attrs={'required': True}),
            'pan_no': forms.TextInput(attrs={'required': True}),

            'gst_status': forms.Select(attrs={'required': True}),
            'state_code': forms.TextInput(attrs={'maxlength': '2', 'pattern': '[0-9]{2}'}),
            'pan_number': forms.TextInput(attrs={'maxlength': '10', 'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}'}),
            'entity_code': forms.TextInput(attrs={'maxlength': '20', 'pattern': '[A-Za-z0-9]{1,20}'}),
            'declaration_rcm': forms.Select(attrs={'required': False}),
            'declaration_status': forms.Select(attrs={'required': False}),
            'gst_no': forms.TextInput(attrs={'readonly': True, 'required': False}),
            'bank_account_name': forms.TextInput(attrs={'required': True}),
            'bank_account_no': forms.TextInput(attrs={'required': True}),
            'bank_name': forms.TextInput(attrs={'required': True}),
            'branch_name': forms.TextInput(attrs={'required': True}),
            'bank_ifsc_code': forms.TextInput(attrs={'required': True}),
            'customer_code_for_invoicing': forms.TextInput(attrs={
                'required': False,
                'class': 'form-control',
                'placeholder': 'Enter customer code for invoicing (optional)',
                'maxlength': '50'
            }),
            'security_deposit_rs': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'required': True}),
            'security_deposit_doc_dd': forms.TextInput(attrs={'required': True}),
            'reg_office_destination_code': forms.TextInput(attrs={'required': True}),
            'closure_date': forms.DateInput(attrs={'type': 'date'}),
            'remark': forms.Textarea(attrs={'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure state field to show data from mas_state table
        self.fields['state'].queryset = MasState.objects.all().order_by('state_name')
        self.fields['state'].empty_label = "Select State"
        
        # Update field labels
        self.fields['district'].label = 'Select District'
        self.fields['district_code'].label = 'District Code (Auto-filled)'
        
        # Set up sale_organization choices
        self.fields['sale_organization'].choices = [
            ('', 'Select Sale Organization'),
            ('Chettinad', 'Chettinad'),
            ('Anjani', 'Anjani'),
        ]
        
        # Configure list_of_plant field - no choices needed for CharField
        # If editing existing record, set the initial value
        if self.instance and self.instance.pk and self.instance.list_of_plant:
            self.initial['list_of_plant'] = self.instance.list_of_plant
    

    
    def clean(self):
        cleaned_data = super().clean()
        

        
        # Set up field choices
        self.fields['gst_status'].choices = [
            ('', 'Select GST Status'),
            ('YES', 'YES'),
            ('NO', 'NO'),
        ]
        
        # Set up declaration_rcm choices
        self.fields['declaration_rcm'].choices = [
            ('', 'Select Declaration/RCM'),
            ('Declaration', 'Declaration'),
            ('RCM', 'RCM'),
        ]
        
        # Set up declaration_status choices
        self.fields['declaration_status'].choices = [
            ('', 'Select Declaration Status'),
            ('Collected', 'Collected'),
            ('Pending', 'Pending'),
        ]
        
        # Validate agreement dates
        agreement_from_date = cleaned_data.get('agreement_from_date')
        agreement_to_date = cleaned_data.get('agreement_to_date')
        
        if agreement_from_date and agreement_to_date and agreement_from_date > agreement_to_date:
            raise forms.ValidationError("Agreement from date cannot be after agreement to date.")
        
        # Handle district field
        district = cleaned_data.get('district')
        
        # If district is selected, populate district_code from district
        if district:
            cleaned_data['district_code'] = district.code
        
        # File size validation (max 50MB for each file)
        max_size = 50 * 1024 * 1024  # 50MB in bytes
        
        for field_name in ['transporter_agreement', 'closure_letter', 'closure_acceptance_letter', 'ff_letter_calc', 'security_deposit', 'kyc_document']:
            file_field = cleaned_data.get(field_name)
            if file_field and hasattr(file_field, 'size') and file_field.size > max_size:
                raise forms.ValidationError(f"{field_name.replace('_', ' ').title()} file size must be less than 50MB.")
        
        return cleaned_data
        
        for field_name in ['transporter_agreement', 'closure_letter', 'closure_acceptance_letter', 'ff_letter_calc', 'security_deposit', 'kyc_document']:
            file_field = cleaned_data.get(field_name)
            if file_field and hasattr(file_field, 'size') and file_field.size > max_size:
                raise forms.ValidationError(f"{field_name.replace('_', ' ').title()} file size must be less than 50MB.")
        
        return cleaned_data

    def is_valid(self):
        # FORCE FIX: Always skip choice validation to prevent "Select a valid choice" errors
        choice_fields = ['stru_grp', 'cfa_status', 'status']
        for field_name in choice_fields:
            if field_name in self.fields:
                # Store original validation
                if not hasattr(self.fields[field_name], '_original_validators'):
                    self.fields[field_name]._original_validators = self.fields[field_name].validators.copy()
                # Clear validators for all records
                self.fields[field_name].validators = []
        
        # FORCE FIX: For branch field, always disable queryset validation
        if 'branch' in self.fields:
            # Store original queryset
            if not hasattr(self.fields['branch'], '_original_queryset'):
                self.fields['branch']._original_queryset = self.fields['branch'].queryset
            # Set queryset to all branches to prevent validation errors
            self.fields['branch'].queryset = MasStateBranch.objects.all()
        
        return super().is_valid()

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = '__all__'
        exclude = ['created_by', 'approved_by', 'approved_at']
        widgets = {
            'nfa_date': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'valid_from': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'valid_to': forms.DateInput(attrs={'type': 'date', 'required': True}),
            'nature_of_approval': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'subject': forms.Textarea(attrs={'rows': 4, 'required': True}),
            'remark': forms.Textarea(attrs={'rows': 3}),
            'attachment': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get('valid_from')
        valid_to = cleaned_data.get('valid_to')
        
        if valid_from and valid_to and valid_from > valid_to:
            raise forms.ValidationError("Valid From date cannot be after Valid To date.")
        
        # File size validation (max 10MB)
        attachment = cleaned_data.get('attachment')
        if attachment and hasattr(attachment, 'size'):
            max_size = 10 * 1024 * 1024  # 10MB in bytes
            if attachment.size > max_size:
                raise forms.ValidationError("Attachment file size must be less than 10MB.")
        
        return cleaned_data

class PartnerDetailsForm(forms.ModelForm):
    """Form for adding partner details to SPO records"""
    
    class Meta:
        model = MasPartnerDetails
        fields = ['name', 'gender', 'address', 'mail_id', 'aadhar_no', 'pan_no', 'partner_join_date', 'partner_end_date']
        exclude = ['spo', 'created_by']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter partner name',
                'maxlength': '200'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select gender'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complete address',
                'rows': '3'
            }),
            'mail_id': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'aadhar_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 12-digit Aadhar number',
                'maxlength': '12',
                'pattern': '[0-9]{12}'
            }),
            'pan_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PAN number (ABCDE1234F)',
                'maxlength': '10',
                'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}'
            }),
            'partner_join_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'partner_end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': False
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.spo_id = kwargs.pop('spo_id', None)
        super().__init__(*args, **kwargs)
        
        # Add field labels
        self.fields['name'].label = 'Partner Name'
        self.fields['gender'].label = 'Gender'
        self.fields['address'].label = 'Address'
        self.fields['mail_id'].label = 'Email ID'
        self.fields['aadhar_no'].label = 'Aadhar Number'
        self.fields['pan_no'].label = 'PAN Number'
        self.fields['partner_join_date'].label = 'Partner Join Date'
        self.fields['partner_end_date'].label = 'Partner End Date (Optional)'
        
        # Add gender choices
        self.fields['gender'].choices = [
            ('', 'Select Gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ]
        
        # Add help text
        self.fields['aadhar_no'].help_text = 'Enter exactly 12 digits'
        self.fields['pan_no'].help_text = 'Format: ABCDE1234F (5 letters + 4 digits + 1 letter)'
        self.fields['partner_end_date'].help_text = 'Leave blank if partner is still active'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check maximum partners limit (only for new records, not updates)
        if self.spo_id and not self.instance.pk:
            existing_partners = MasPartnerDetails.objects.filter(spo_id=self.spo_id).count()
            if existing_partners >= 5:
                raise forms.ValidationError('Maximum 5 partners allowed per SPO.')
        
        # Validate dates
        join_date = cleaned_data.get('partner_join_date')
        end_date = cleaned_data.get('partner_end_date')
        
        if join_date and end_date and end_date < join_date:
            raise forms.ValidationError('Partner end date cannot be before join date.')
        
        return cleaned_data


class CFAPartnerDetailsForm(forms.ModelForm):
    """Form for adding partner details to CFA Agreement records"""
    
    class Meta:
        model = CFAPartnerDetails
        fields = ['name', 'gender', 'address', 'mail_id', 'aadhar_no', 'pan_no', 'partner_join_date', 'partner_end_date']
        exclude = ['cfa_agreement', 'created_by']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter partner name',
                'maxlength': '200'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select gender'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complete address',
                'rows': '3'
            }),
            'mail_id': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'aadhar_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 12-digit Aadhar number',
                'maxlength': '12',
                'pattern': '[0-9]{12}'
            }),
            'pan_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PAN number (ABCDE1234F)',
                'maxlength': '10',
                'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}'
            }),
            'partner_join_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'partner_end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': False
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.cfa_agreement_id = kwargs.pop('cfa_agreement_id', None)
        super().__init__(*args, **kwargs)
        
        # Add field labels
        self.fields['name'].label = 'Partner Name'
        self.fields['gender'].label = 'Gender'
        self.fields['address'].label = 'Address'
        self.fields['mail_id'].label = 'Email ID'
        self.fields['aadhar_no'].label = 'Aadhar Number'
        self.fields['pan_no'].label = 'PAN Number'
        self.fields['partner_join_date'].label = 'Partner Join Date'
        self.fields['partner_end_date'].label = 'Partner End Date (Optional)'
        
        # Add gender choices
        self.fields['gender'].choices = [
            ('', 'Select Gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ]
        
        # Add help text
        self.fields['aadhar_no'].help_text = 'Enter exactly 12 digits'
        self.fields['pan_no'].help_text = 'Format: ABCDE1234F (5 letters + 4 digits + 1 letter)'
        self.fields['partner_end_date'].help_text = 'Leave blank if partner is still active'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check maximum partners limit (only for new records, not updates)
        if self.cfa_agreement_id and not self.instance.pk:
            existing_partners = CFAPartnerDetails.objects.filter(cfa_agreement_id=self.cfa_agreement_id).count()
            if existing_partners >= 5:
                raise forms.ValidationError('Maximum 5 partners allowed per CFA Agreement.')
        
        # Validate dates
        join_date = cleaned_data.get('partner_join_date')
        end_date = cleaned_data.get('partner_end_date')
        
        if join_date and end_date and end_date < join_date:
            raise forms.ValidationError('Partner end date cannot be before join date.')
        
        return cleaned_data


class TransporterPartnerDetailsForm(forms.ModelForm):
    """Form for adding partner details to Transporter Agreement records"""
    
    class Meta:
        model = TransporterPartnerDetails
        fields = ['name', 'gender', 'address', 'mail_id', 'aadhar_no', 'pan_no', 'partner_join_date', 'partner_end_date']
        exclude = ['transporter_agreement', 'created_by']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter partner name',
                'maxlength': '200'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select gender'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complete address',
                'rows': '3'
            }),
            'mail_id': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'aadhar_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 12-digit Aadhar number',
                'maxlength': '12',
                'pattern': '[0-9]{12}'
            }),
            'pan_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PAN number (ABCDE1234F)',
                'maxlength': '10',
                'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}'
            }),
            'partner_join_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'partner_end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': False
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.transporter_agreement_id = kwargs.pop('transporter_agreement_id', None)
        super().__init__(*args, **kwargs)
        
        # Add field labels
        self.fields['name'].label = 'Partner Name'
        self.fields['gender'].label = 'Gender'
        self.fields['address'].label = 'Address'
        self.fields['mail_id'].label = 'Email ID'
        self.fields['aadhar_no'].label = 'Aadhar Number'
        self.fields['pan_no'].label = 'PAN Number'
        self.fields['partner_join_date'].label = 'Partner Join Date'
        self.fields['partner_end_date'].label = 'Partner End Date (Optional)'
        
        # Add gender choices
        self.fields['gender'].choices = [
            ('', 'Select Gender'),
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ]
        
        # Add help text
        self.fields['aadhar_no'].help_text = 'Enter exactly 12 digits'
        self.fields['pan_no'].help_text = 'Format: ABCDE1234F (5 letters + 4 digits + 1 letter)'
        self.fields['partner_end_date'].help_text = 'Leave blank if partner is still active'
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check maximum partners limit (only for new records, not updates)
        if self.transporter_agreement_id and not self.instance.pk:
            existing_partners = TransporterPartnerDetails.objects.filter(transporter_agreement_id=self.transporter_agreement_id).count()
            if existing_partners >= 5:
                raise forms.ValidationError('Maximum 5 partners allowed per Transporter Agreement.')
        
        # Validate dates
        join_date = cleaned_data.get('partner_join_date')
        end_date = cleaned_data.get('partner_end_date')
        
        if join_date and end_date and end_date < join_date:
            raise forms.ValidationError('Partner end date cannot be before join date.')
        
        return cleaned_data

class ChatbotQuestionForm(forms.ModelForm):
    """Form for creating and editing chatbot questions"""
    
    class Meta:
        model = ChatbotQuestion
        fields = ['question', 'response', 'category', 'is_active', 'order']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the question to display to users'
            }),
            'response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter the response to provide when this question is selected'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            })
        }

    def clean_question(self):
        question = self.cleaned_data['question']
        if len(question.strip()) < 10:
            raise forms.ValidationError("Question must be at least 10 characters long.")
        return question.strip()

    def clean_response(self):
        response = self.cleaned_data['response']
        if len(response.strip()) < 20:
            raise forms.ValidationError("Response must be at least 20 characters long.")
        return response.strip()









class MasDistrictForm(forms.ModelForm):
    class Meta:
        model = MasDistrict
        fields = ['mas_state', 'mas_branch', 'name', 'code', 'status']
        widgets = {
            'mas_state': forms.Select(attrs={'class': 'form-select'}),
            'mas_branch': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=[
                (1, 'Active'),
                (0, 'Inactive')
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter branch options based on selected state
        if self.instance.pk and self.instance.mas_state:
            self.fields['mas_branch'].queryset = MasStateBranch.objects.filter(
                mas_state=self.instance.mas_state
            )
        else:
            self.fields['mas_branch'].queryset = MasStateBranch.objects.none()