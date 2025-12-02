from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings

# Create your models here.

# Models for the manually created tables
class MasState(models.Model):
    """Model for mas_state table"""
    id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=100, unique=True)
    state_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    status = models.IntegerField(default=1)  # 1 for Active, 0 for Inactive
    
    class Meta:
        db_table = 'mas_state'
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ['state_name']
    
    def __str__(self):
        return self.state_name

class MasStateBranch(models.Model):
    """Model for mas_state_branch table"""
    id = models.AutoField(primary_key=True)
    state = models.ForeignKey(MasState, on_delete=models.CASCADE, db_column='state_id')
    state_branch_name = models.CharField(max_length=100)
    state_branch_code = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'mas_state_branch'
        verbose_name = "State Branch"
        verbose_name_plural = "State Branches"
        ordering = ['state__state_name', 'state_branch_name']
    
    def __str__(self):
        return f"{self.state_branch_name} ({self.state.state_name})"

class MasConstruction(models.Model):
    """Model for mas_construction table"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    remark = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=1)  # 1 for Active, 0 for Inactive
    
    class Meta:
        db_table = 'mas_construction'
        verbose_name = "Construction Type"
        verbose_name_plural = "Construction Types"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class MasPartner(models.Model):
    """Model for mas_partner table"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    remark = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=1)  # 1 for Active, 0 for Inactive
    
    class Meta:
        db_table = 'mas_partner'
        verbose_name = "Partner Type"
        verbose_name_plural = "Partner Types"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class MasPlant(models.Model):
    """Model for mas_plant table"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Plant Code")
    status = models.IntegerField(default=1)  # 1 for Active, 0 for Inactive
    
    class Meta:
        db_table = 'mas_plant'
        verbose_name = "Plant"
        verbose_name_plural = "Plants"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}"

class MasPartnerDetails(models.Model):
    """Model for mas_partner_details table - stores partner details for each SPO"""
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    id = models.AutoField(primary_key=True)
    spo = models.ForeignKey('SPORent', on_delete=models.CASCADE, related_name='partners', verbose_name="SPO")
    name = models.CharField(max_length=200, verbose_name="Partner Name")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    address = models.TextField(verbose_name="Address")
    mail_id = models.EmailField(verbose_name="Email ID")
    aadhar_no = models.CharField(max_length=12, verbose_name="Aadhar Number")
    pan_no = models.CharField(max_length=10, verbose_name="PAN Number")
    partner_join_date = models.DateField(verbose_name="Partner Join Date")
    partner_end_date = models.DateField(verbose_name="Partner End Date", null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='partners_created')
    
    class Meta:
        db_table = 'spo_partner_details'
        verbose_name = "Partner Detail"
        verbose_name_plural = "Partner Details"
        ordering = ['-created_at']
        unique_together = ['spo', 'aadhar_no']  # Each Aadhar number can only be associated with one SPO
    
    def __str__(self):
        return f"{self.name} - {self.spo.spo_code}"


class CFAPartnerDetails(models.Model):
    """Model for cfa_partner_details table - stores partner details for each CFA Agreement"""
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    id = models.AutoField(primary_key=True)
    cfa_agreement = models.ForeignKey('CFAAgreement', on_delete=models.CASCADE, related_name='partners', verbose_name="CFA Agreement")
    name = models.CharField(max_length=200, verbose_name="Partner Name")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    address = models.TextField(verbose_name="Address")
    mail_id = models.EmailField(verbose_name="Email ID")
    aadhar_no = models.CharField(max_length=12, verbose_name="Aadhar Number")
    pan_no = models.CharField(max_length=10, verbose_name="PAN Number")
    partner_join_date = models.DateField(verbose_name="Partner Join Date")
    partner_end_date = models.DateField(verbose_name="Partner End Date", null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cfa_partners_created')
    
    class Meta:
        db_table = 'cfa_partner_details'
        verbose_name = "CFA Partner Detail"
        verbose_name_plural = "CFA Partner Details"
        ordering = ['-created_at']
        unique_together = ['cfa_agreement', 'aadhar_no']  # Each Aadhar number can only be associated with one CFA Agreement
    
    def __str__(self):
        return f"{self.name} - {self.cfa_agreement.cfa_code}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        import re
        
        # Validate Aadhar number (12 digits)
        if not re.match(r'^\d{12}$', self.aadhar_no):
            raise ValidationError({'aadhar_no': 'Aadhar number must be exactly 12 digits.'})
        
        # Validate PAN number (10 characters: 5 letters + 4 digits + 1 letter)
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', self.pan_no):
            raise ValidationError({'pan_no': 'PAN number must be in format: ABCDE1234F'})
        
        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.mail_id):
            raise ValidationError({'mail_id': 'Please enter a valid email address.'})
        
        # Check if partner end date is after join date
        if self.partner_end_date and self.partner_end_date < self.partner_join_date:
            raise ValidationError({'partner_end_date': 'Partner end date cannot be before join date.'})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        import re
        
        # Validate Aadhar number (12 digits)
        if not re.match(r'^\d{12}$', self.aadhar_no):
            raise ValidationError({'aadhar_no': 'Aadhar number must be exactly 12 digits.'})
        
        # Validate PAN number (10 characters: 5 letters + 4 digits + 1 letter)
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', self.pan_no):
            raise ValidationError({'pan_no': 'PAN number must be in format: ABCDE1234F'})
        
        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.mail_id):
            raise ValidationError({'mail_id': 'Please enter a valid email address.'})
        
        # Check if partner end date is after join date
        if self.partner_end_date and self.partner_end_date < self.partner_join_date:
            raise ValidationError({'partner_end_date': 'Partner end date cannot be before join date.'})
        
        # Note: Partner limit check is handled in the form's clean method
        # to avoid circular import issues and ensure proper validation
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class TransporterPartnerDetails(models.Model):
    """Model for transporter_partner_details table - stores partner details for each Transporter Agreement"""
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    id = models.AutoField(primary_key=True)
    transporter_agreement = models.ForeignKey('TransporterAgreement', on_delete=models.CASCADE, related_name='partners', verbose_name="Transporter Agreement")
    name = models.CharField(max_length=200, verbose_name="Partner Name")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    address = models.TextField(verbose_name="Address")
    mail_id = models.EmailField(verbose_name="Email ID")
    aadhar_no = models.CharField(max_length=12, verbose_name="Aadhar Number")
    pan_no = models.CharField(max_length=10, verbose_name="PAN Number")
    partner_join_date = models.DateField(verbose_name="Partner Join Date")
    partner_end_date = models.DateField(verbose_name="Partner End Date", null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transporter_partners_created')
    
    class Meta:
        db_table = 'transporter_partner_details'
        verbose_name = "Transporter Partner Detail"
        verbose_name_plural = "Transporter Partner Details"
        ordering = ['-created_at']
        unique_together = ['transporter_agreement', 'aadhar_no']  # Each Aadhar number can only be associated with one Transporter Agreement
    
    def __str__(self):
        return f"{self.name} - {self.transporter_agreement.transporter_code}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        import re
        
        # Validate Aadhar number (12 digits)
        if not re.match(r'^\d{12}$', self.aadhar_no):
            raise ValidationError({'aadhar_no': 'Aadhar number must be exactly 12 digits.'})
        
        # Validate PAN number (10 characters: 5 letters + 4 digits + 1 letter)
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', self.pan_no):
            raise ValidationError({'pan_no': 'PAN number must be in format: ABCDE1234F'})
        
        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.mail_id):
            raise ValidationError({'mail_id': 'Please enter a valid email address.'})
        
        # Check if partner end date is after join date
        if self.partner_end_date and self.partner_end_date < self.partner_join_date:
            raise ValidationError({'partner_end_date': 'Partner end date cannot be before join date.'})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class IndianState(models.Model):
    """Model to store all Indian states and union territories"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    is_union_territory = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Indian State"
        verbose_name_plural = "Indian States"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class MasDistrict(models.Model):
    """Model for managing districts that map to states and state branches"""
    id = models.AutoField(primary_key=True)
    mas_state = models.ForeignKey(MasState, on_delete=models.CASCADE, related_name='districts')
    mas_branch = models.ForeignKey(MasStateBranch, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    status = models.IntegerField(default=1, choices=[
        (1, 'Active'),
        (0, 'Inactive')
    ])
    
    class Meta:
        db_table = 'mas_district'
        ordering = ['name']
        verbose_name = 'District'
        verbose_name_plural = 'Districts'
    
    def __str__(self):
        return f"{self.name} - {self.mas_branch.state_branch_name} ({self.mas_state.state_name})"
    
    def get_full_path(self):
        """Get the full hierarchical path: State > Branch > District"""
        return f"{self.mas_state.state_name} > {self.mas_branch.state_branch_name} > {self.name}"

class SPORent(models.Model):
    # Basic Information - MANDATORY FIELDS
    sale_organization = models.CharField(max_length=50, choices=[
        ('Chettinad', 'Chettinad'),
        ('Anjani', 'Anjani'),
    ], verbose_name="Sale Organization", null=True, blank=True)
    spo_code = models.CharField(max_length=4, unique=True, verbose_name="SPO Code", help_text="Maximum 4 characters")
    state = models.ForeignKey(MasState, on_delete=models.CASCADE, verbose_name="State")
    branch = models.ForeignKey(MasStateBranch, on_delete=models.CASCADE, verbose_name="Branch", null=True, blank=True)
    district = models.ForeignKey(MasDistrict, on_delete=models.SET_NULL, verbose_name="District", null=True, blank=True)
    district_code = models.CharField(max_length=20, null=True, blank=True)
    spo_name = models.CharField(max_length=200, null=True, blank=True)
    stru_grp = models.CharField(max_length=100, choices=[
        ('Road', 'Road'),
        ('Rail', 'Rail'),
        ('TDP', 'TDP'),
        ('Others', 'Others'),
    ], verbose_name="Structure Group", null=True, blank=True)
    cfa_status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Notice', 'Under Notice'),
        ('Closed', 'Closed'),
    ], verbose_name="SPO Status", null=True, blank=True)
    
    # Agreement Details - MANDATORY FIELDS
    inception_date = models.DateField(null=True, blank=True)
    renewal_with = models.CharField(max_length=50, choices=[
        ('Agreement', 'Agreement'),
        ('Renewal', 'Renewal'),
    ], verbose_name="Renewal With", null=True, blank=True)
    
    # Owner Information - MANDATORY FIELDS
    godown_address = models.TextField(null=True, blank=True)
    owner_name = models.CharField(max_length=200, null=True, blank=True)
    owner_contact_no = models.CharField(max_length=20, null=True, blank=True)
    owner_code = models.CharField(max_length=50, verbose_name="Owner Code", null=True, blank=True)
    owner_address = models.TextField(verbose_name="Owner Address", null=True, blank=True)
    owner_gst = models.CharField(max_length=20, verbose_name="Owner GST", null=True, blank=True)
    gst_status = models.CharField(max_length=10, choices=[
        ('YES', 'YES'),
        ('NO', 'NO'),
    ], verbose_name="GST Status", null=True, blank=True)
    state_code = models.CharField(max_length=2, verbose_name="State Code", null=True, blank=True)
    pan_number = models.CharField(max_length=10, verbose_name="PAN Number", null=True, blank=True)
    entity_code = models.CharField(max_length=20, verbose_name="Last 5 Characters", null=True, blank=True)
    declaration_rcm = models.CharField(max_length=20, choices=[
        ('Declaration', 'Declaration'),
        ('RCM', 'RCM'),
    ], verbose_name="Declaration / RCM", null=True, blank=True)
    declaration_status = models.CharField(max_length=10, choices=[
        ('Collected', 'Collected'),
        ('Pending', 'Pending'),
    ], verbose_name="Declaration Status", null=True, blank=True)
    owner_pan = models.CharField(max_length=20, verbose_name="Owner PAN", null=True, blank=True)
    pin_code = models.CharField(max_length=10, verbose_name="Pin Code", null=True, blank=True)
    nature_of_construction = models.ForeignKey(MasConstruction, on_delete=models.SET_NULL, verbose_name="Nature of Construction", null=True, blank=True)
    stamp_no = models.CharField(max_length=50, verbose_name="Stamp No", null=True, blank=True)
    stamp_name = models.CharField(max_length=200, verbose_name="Stamp Name", null=True, blank=True)
    partner_type = models.ForeignKey(MasPartner, on_delete=models.SET_NULL, verbose_name="Partner Type", null=True, blank=True)
    new_partner_type = models.CharField(max_length=100, verbose_name="New Partner Type", null=True, blank=True)
    capacity_mt = models.CharField(max_length=50, verbose_name="Capacity (In Mt)", null=True, blank=True)

    cfa_mail_id = models.EmailField(verbose_name="Owner Mail ID", null=True, blank=True)
    
    # Bank Information - NON-MANDATORY FIELDS
    bank_account_name = models.CharField(max_length=200, null=True, blank=True)
    bank_account_no = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=200, null=True, blank=True)
    bank_branch_name = models.CharField(max_length=200, null=True, blank=True)
    bank_ifsc_code = models.CharField(max_length=20, null=True, blank=True)
    
    # Financial Details - NON-MANDATORY FIELDS
    destination_code = models.CharField(max_length=50, verbose_name="Depot Sq.Ft", null=True, blank=True)
    office_sqft = models.CharField(max_length=50, verbose_name="Office Sq.ft", null=True, blank=True)
    open_space_sqft = models.CharField(max_length=50, verbose_name="Open Space Sq.ft", null=True, blank=True)
    
    # Additional Space and Capacity Details - NON-MANDATORY FIELDS
    total_space = models.CharField(max_length=50, verbose_name="Total Space", null=True, blank=True)
    capacity = models.CharField(max_length=50, verbose_name="Capacity", null=True, blank=True)
    rental_from_date = models.DateField(verbose_name="From Date", null=True, blank=True)
    rental_to_date = models.DateField(verbose_name="To Date", null=True, blank=True)
    days_count = models.IntegerField(verbose_name="Days Count", null=True, blank=True)
    security_deposit_paid = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Security Deposit Paid", null=True, blank=True)
    security_deposit_doc = models.CharField(max_length=200, verbose_name="Security Deposit Doc. / Ref. / DD", null=True, blank=True)
    rent_pm = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Rent PM", null=True, blank=True)
    yearly_hike_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Yearly Hike %", null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, verbose_name="Latitude", null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, verbose_name="Longitude", null=True, blank=True)
    vacation_letter = models.FileField(upload_to='spo_rent_attachments/', verbose_name="Vacation Letter", help_text='Vacation Letter (Max file size: 10 MB)', null=True, blank=True)
    
    # Additional Information - NON-MANDATORY FIELDS
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Notice', 'Under Notice'),
        ('Closed', 'Closed'),
    ], null=True, blank=True)
    
    # Documents/Attachments - NON-MANDATORY FIELDS
    transporter_agreement = models.FileField(upload_to='spo_rent_attachments/', verbose_name='Rent Agreement', help_text='Rent Agreement (Max file size: 50 MB)', null=True, blank=True)
    closure_letter = models.FileField(upload_to='spo_rent_attachments/', help_text='Closure Letter (Max file size: 50 MB)', null=True, blank=True)
    closure_acceptance_letter = models.FileField(upload_to='spo_rent_attachments/', help_text='Closure Acceptance Letter (Max file size: 50 MB)', null=True, blank=True)
    ff_letter_calc = models.FileField(upload_to='spo_rent_attachments/', help_text='F&F Letter & Calc. (Max file size: 50 MB)', null=True, blank=True)
    security_deposit = models.FileField(upload_to='spo_rent_attachments/', help_text='Security Deposit (Max file size: 50 MB)', null=True, blank=True)
    kyc_document = models.FileField(upload_to='spo_rent_attachments/', verbose_name='KYC Document', help_text='KYC Document (Max file size: 50 MB)', null=True, blank=True)
    consolidate_document = models.FileField(upload_to='spo_rent_attachments/', verbose_name='Consolidate Document', help_text='Consolidate Document (Max file size: 50 MB)', null=True, blank=True)
    bank_details = models.FileField(upload_to='spo_rent_attachments/', verbose_name='Bank Details', help_text='Bank Details Document (Max file size: 50 MB)', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate days count if rental_from_date and rental_to_date are provided
        if self.rental_from_date and self.rental_to_date:
            self.days_count = (self.rental_to_date - self.rental_from_date).days + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "SPO Rent"
        verbose_name_plural = "SPO Rents"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.spo_name} - {self.spo_code}"
    


class CFAAgreement(models.Model):
    # Basic Information
    state = models.ForeignKey(MasState, on_delete=models.CASCADE, verbose_name="State")
    branch = models.ForeignKey(MasStateBranch, on_delete=models.CASCADE, verbose_name="Branch", null=True, blank=True)
    district = models.ForeignKey(MasDistrict, on_delete=models.SET_NULL, verbose_name="District", null=True, blank=True)
    district_code = models.CharField(max_length=20)
    sale_organization = models.CharField(max_length=50, choices=[
        ('Chettinad', 'Chettinad'),
        ('Anjani', 'Anjani'),
    ], verbose_name="Sale Organization", null=True, blank=True)
    spo_code = models.CharField(max_length=50)
    spo_name = models.CharField(max_length=200)
    stru_grp = models.CharField(max_length=100, choices=[
        ('Road', 'Road'),
        ('Rail', 'Rail'),
        ('TDP', 'TDP'),
        ('Others', 'Others'),
    ])
    cfa_status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Notice', 'Under Notice'),
        ('Closed', 'Closed'),
    ])
    
    # Agreement Details
    agreement_renewal = models.CharField(max_length=50, choices=[
        ('Agreement', 'Agreement'),
        ('Renewal', 'Renewal'),
    ])
    inception_date = models.DateField()
    agreement_from_date = models.DateField()
    agreement_to_date = models.DateField()
    
    # CFA Information
    godown_address = models.TextField()
    cfa_code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    cfa_name = models.CharField(max_length=200)
    cfa_address = models.TextField()
    owner_name = models.CharField(max_length=200)
    owner_contact_no = models.CharField(max_length=20)
    cfa_mail_id = models.EmailField()
    
    # Business Details
    gst_no = models.CharField(max_length=20, null=True, blank=True)
    pan_no = models.CharField(max_length=20)
    
    # GST Status Fields
    gst_status = models.CharField(max_length=10, choices=[
        ('YES', 'YES'),
        ('NO', 'NO'),
    ], verbose_name="GST Status", null=True, blank=True)
    state_code = models.CharField(max_length=2, verbose_name="State Code", null=True, blank=True)
    pan_number = models.CharField(max_length=10, verbose_name="PAN Number", null=True, blank=True)
    entity_code = models.CharField(max_length=20, verbose_name="Last 5 Characters", null=True, blank=True)
    declaration_rcm = models.CharField(max_length=20, choices=[
        ('Declaration', 'Declaration'),
        ('RCM', 'RCM'),
    ], verbose_name="Declaration / RCM", null=True, blank=True)
    declaration_status = models.CharField(max_length=10, choices=[
        ('Collected', 'Collected'),
        ('Pending', 'Pending'),
    ], verbose_name="Declaration Status", null=True, blank=True)
    
    # Bank Information
    bank_account_name = models.CharField(max_length=200)
    bank_account_no = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=200)
    bank_branch_name = models.CharField(max_length=200, null=True, blank=True)
    bank_ifsc_code = models.CharField(max_length=20)
    
    # Financial Details
    destination_code = models.CharField(max_length=50)
    security_deposit_rs = models.DecimalField(max_digits=12, decimal_places=2)
    security_deposit_doc_ref_dd = models.CharField(max_length=200, null=True, blank=True)
    
    # Additional Information
    closure_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    customer_code = models.CharField(max_length=50, verbose_name="Customer Code", null=True, blank=True)
    
    # Documents
    cfa_agreement = models.FileField(upload_to='cfa_agreements/', null=True, blank=True)
    closure_letter = models.FileField(upload_to='cfa_agreements/', null=True, blank=True)
    closure_acceptance_letter = models.FileField(upload_to='cfa_agreements/', null=True, blank=True)
    ff_letter_calc = models.FileField(upload_to='cfa_agreements/', null=True, blank=True)
    security_deposit = models.FileField(upload_to='cfa_agreements/', null=True, blank=True)
    kyc_document = models.FileField(upload_to='cfa_agreements/', null=True, blank=True, verbose_name="KYC Document", help_text='KYC Document (Max file size: 50 MB)')
    consolidate_attachment = models.FileField(upload_to='cfa_agreements/', null=True, blank=True, verbose_name="Consolidate Attachment", help_text='Consolidate Attachment (Max file size: 50 MB)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CFA Agreement"
        verbose_name_plural = "CFA Agreements"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.cfa_name} - {self.cfa_code}"

class TransporterAgreement(models.Model):
    # Basic Information
    state = models.ForeignKey(MasState, on_delete=models.CASCADE, verbose_name="State")
    district = models.ForeignKey(MasDistrict, on_delete=models.SET_NULL, verbose_name="District", null=True, blank=True)
    district_code = models.CharField(max_length=20, null=True, blank=True)
    sale_organization = models.CharField(max_length=50, choices=[
        ('Chettinad', 'Chettinad'),
        ('Anjani', 'Anjani'),
    ], verbose_name="Sale Organization", null=True, blank=True)
    source_plant_code = models.CharField(max_length=50)
    source_plant_name = models.CharField(max_length=200)
    operating_in_multiple_plant = models.CharField(max_length=10, choices=[
        ('Yes', 'Yes'),
        ('No', 'No'),
    ])
    list_of_plant = models.CharField(max_length=500, blank=True, null=True, verbose_name="List of Plant", help_text="Select multiple plants separated by commas")
    transporter_status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Close', 'Close'),
    ])
    
    # Agreement Details
    inception_date = models.DateField()
    agreement_from_date = models.DateField()
    agreement_to_date = models.DateField()
    
    # Transporter Information
    transporter_code = models.CharField(max_length=50, unique=True)
    transporter_name = models.CharField(max_length=200)
    transporter_address = models.TextField()
    pincode = models.CharField(max_length=10, verbose_name="PIN Code")
    owner_managing_partner = models.CharField(max_length=200)
    owner_contact_no = models.CharField(max_length=20)
    transporter_mail_id = models.EmailField()
    
    # Business Details
    gst_no = models.CharField(max_length=20, blank=True, null=True, verbose_name="GST Number")
    pan_no = models.CharField(max_length=20)
    
    # Approval Information

    
    # GST Status Information
    gst_status = models.CharField(max_length=3, choices=[
        ('YES', 'YES'),
        ('NO', 'NO'),
    ], verbose_name="GST Status")
    state_code = models.CharField(max_length=2, blank=True, null=True, verbose_name="State Code")
    pan_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="PAN Number")
    entity_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Entity Code")
    declaration_rcm = models.CharField(max_length=20, choices=[
        ('Declaration', 'Declaration'),
        ('RCM', 'RCM'),
    ], blank=True, null=True, verbose_name="Declaration/RCM")
    declaration_status = models.CharField(max_length=20, choices=[
        ('Collected', 'Collected'),
        ('Pending', 'Pending'),
    ], blank=True, null=True, verbose_name="Declaration Status")
    
    # Bank Information
    bank_account_name = models.CharField(max_length=200)
    bank_account_no = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=200)
    branch_name = models.CharField(max_length=200)
    bank_ifsc_code = models.CharField(max_length=20)
    
    # Financial Details
    customer_code_for_invoicing = models.CharField(max_length=50, null=True, blank=True)
    security_deposit_rs = models.DecimalField(max_digits=12, decimal_places=2)
    security_deposit_doc_dd = models.CharField(max_length=200)
    
    # Additional Information
    reg_office_destination_code = models.CharField(max_length=50)
    closure_date = models.DateField(null=True, blank=True)
    remark = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Under Notice', 'Under Notice'),
        ('Closed', 'Closed'),
    ])
    
    # Documents
    transporter_agreement = models.FileField(upload_to='transporter_agreements/', null=True, blank=True)
    closure_letter = models.FileField(upload_to='transporter_agreements/', null=True, blank=True)
    closure_acceptance_letter = models.FileField(upload_to='transporter_agreements/', null=True, blank=True)
    ff_letter_calc = models.FileField(upload_to='transporter_agreements/', null=True, blank=True)
    security_deposit = models.FileField(upload_to='transporter_agreements/', null=True, blank=True)
    kyc_document = models.FileField(upload_to='transporter_agreements/', null=True, blank=True, verbose_name="KYC Document")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Transporter Agreement"
        verbose_name_plural = "Transporter Agreements"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transporter_name} - {self.transporter_code}"

class Approval(models.Model):
    """Approval model for managing various types of approvals"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    NATURE_CHOICES = [
        ('plant', 'Plant'),
        ('other', 'Other'),
        ('spo', 'SPO'),
        ('internal', 'Internal'),
        ('dc_wc', 'DC/WC'),
        ('cmd_approval', 'CMD Approval'),
        ('shortage', 'Shortage'),
        ('rp_loss', 'RP Loss'),
        ('halting', 'Halting'),
    ]
    
    # Basic Information
    nfa_no = models.CharField(max_length=50, unique=True, verbose_name="NFA No")
    nfa_date = models.DateField(verbose_name="NFA Date")
    nature_of_approval = models.CharField(max_length=50, choices=NATURE_CHOICES, verbose_name="Nature of Approval")
    code = models.CharField(max_length=50, verbose_name="Code")
    name = models.CharField(max_length=200, verbose_name="Name")
    subject = models.TextField(verbose_name="Subject")
    
    # Validity Period
    valid_from = models.DateField(verbose_name="Valid From")
    valid_to = models.DateField(verbose_name="Valid To")
    
    # Additional Information
    remark = models.TextField(blank=True, verbose_name="Remark")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    
    # Attachments
    attachment = models.FileField(upload_to='approval_attachments/', null=True, blank=True, verbose_name="Attachment", help_text="Upload supporting documents (PDF, DOC, DOCX, JPG, PNG - Max 10MB)")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approvals_created')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approvals_approved')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Approval"
        verbose_name_plural = "Approvals"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.nfa_no} - {self.name}"
    
    def is_expired(self):
        """Check if approval is expired"""
        return self.valid_to < timezone.now().date()
    
    def can_approve(self):
        """Check if approval can be approved"""
        return self.status == 'pending'
    
    def can_reject(self):
        """Check if approval can be rejected"""
        return self.status == 'pending'


class ApprovalWorkflow(models.Model):
    """Model for managing approval workflows for records and partners"""
    RECORD_TYPE_CHOICES = [
        ('spo_rent', 'SPO Rent'),
        ('cfa_agreement', 'CFA Agreement'),
        ('transporter_agreement', 'Transporter Agreement'),
        ('spo_partner', 'SPO Partner'),
        ('cfa_partner', 'CFA Partner'),
        ('transporter_partner', 'Transporter Partner'),
    ]
    
    STATUS_CHOICES = [
        ('waiting_confirmation', 'Waiting for Superior Confirmation'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]
    
    # Record Information
    record_type = models.CharField(max_length=50, choices=RECORD_TYPE_CHOICES, verbose_name="Record Type")
    record_id = models.IntegerField(verbose_name="Record ID")
    record_code = models.CharField(max_length=100, verbose_name="Record Code/Name")
    
    # Approval Information
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='waiting_confirmation', verbose_name="Status")
    approver_remarks = models.TextField(blank=True, verbose_name="Approver Remarks")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Record Creation Date")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Submission Date")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="Approval Date")
    
    # User Information
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='workflows_submitted', verbose_name="Submitted By")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='workflows_approved', verbose_name="Approved By")
    
    # Additional Information
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Approval Workflow"
        verbose_name_plural = "Approval Workflows"
        ordering = ['-created_at']
        unique_together = ['record_type', 'record_id']
        indexes = [
            models.Index(fields=['record_type', 'record_id']),
            models.Index(fields=['status']),
            models.Index(fields=['submitted_by']),
            models.Index(fields=['approved_by']),
        ]
    
    def __str__(self):
        return f"{self.get_record_type_display()} - {self.record_code} ({self.get_status_display()})"
    
    def get_record_object(self):
        """Get the actual record object based on record_type and record_id"""
        try:
            if self.record_type == 'spo_rent':
                return SPORent.objects.get(id=self.record_id)
            elif self.record_type == 'cfa_agreement':
                return CFAAgreement.objects.get(id=self.record_id)
            elif self.record_type == 'transporter_agreement':
                return TransporterAgreement.objects.get(id=self.record_id)
            elif self.record_type == 'spo_partner':
                return MasPartnerDetails.objects.get(id=self.record_id)
            elif self.record_type == 'cfa_partner':
                return CFAPartnerDetails.objects.get(id=self.record_id)
            elif self.record_type == 'transporter_partner':
                return TransporterPartnerDetails.objects.get(id=self.record_id)
        except:
            return None
    
    def approve(self, approver, remarks=""):
        """Approve the workflow"""
        self.status = 'confirmed'
        self.approver_remarks = remarks
        self.approved_by = approver
        self.approved_at = timezone.now()
        self.save()
        
        # Update the actual record status if it has a status field
        record_obj = self.get_record_object()
        if record_obj and hasattr(record_obj, 'status'):
            if hasattr(record_obj, 'approval_status'):
                record_obj.approval_status = 'confirmed'
            record_obj.save()
    
    def reject(self, approver, remarks=""):
        """Reject the workflow"""
        self.status = 'rejected'
        self.approver_remarks = remarks
        self.approved_by = approver
        self.approved_at = timezone.now()
        self.save()
        
        # Update the actual record status if it has a status field
        record_obj = self.get_record_object()
        if record_obj and hasattr(record_obj, 'status'):
            if hasattr(record_obj, 'approval_status'):
                record_obj.approval_status = 'rejected'
            record_obj.save()


class ApprovalWorkflowHistory(models.Model):
    """Model for tracking approval workflow history and changes"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('updated', 'Updated'),
        ('comment_added', 'Comment Added'),
    ]
    
    workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.CASCADE, related_name='history', verbose_name="Workflow")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name="Action")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")
    remarks = models.TextField(blank=True, verbose_name="Remarks")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    
    class Meta:
        verbose_name = "Approval Workflow History"
        verbose_name_plural = "Approval Workflow Histories"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.workflow} - {self.get_action_display()} by {self.user.username if self.user else 'System'}"


# Mail Reminder Management Models
class EmailReminder(models.Model):
    """Model for managing email reminder templates and configurations"""
    REMINDER_TYPE_CHOICES = [
        ('spo_rent_renewal', 'SPO Rent Renewal'),
        ('spo_rent_expiry', 'SPO Rent Expiry'),
        ('spo_rent_payment', 'SPO Rent Payment'),
        ('cfa_agreement_renewal', 'CFA Agreement Renewal'),
        ('cfa_agreement_expiry', 'CFA Agreement Expiry'),
        ('transporter_agreement_renewal', 'Transporter Agreement Renewal'),
        ('transporter_agreement_expiry', 'Transporter Agreement Expiry'),
        ('payment_due', 'Payment Due'),
        ('document_expiry', 'Document Expiry'),
        ('general', 'General Update'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="Reminder Name")
    reminder_type = models.CharField(max_length=50, choices=REMINDER_TYPE_CHOICES, verbose_name="Reminder Type")
    subject_template = models.CharField(max_length=300, verbose_name="Email Subject Template")
    message_template = models.TextField(verbose_name="Email Message Template")
    
    # Configuration
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Status")
    is_automated = models.BooleanField(default=False, verbose_name="Automated Reminder")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reminders_created')
    
    class Meta:
        verbose_name = "Email Reminder"
        verbose_name_plural = "Email Reminders"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_reminder_type_display()})"
    
    def get_recipients_count(self):
        """Get count of potential recipients for this reminder type"""
        if self.reminder_type == 'spo_rent_renewal':
            return SPORent.objects.exclude(cfa_mail_id__isnull=True).exclude(cfa_mail_id='').count()
        elif self.reminder_type == 'cfa_agreement_renewal':
            return CFAAgreement.objects.exclude(cfa_mail_id__isnull=True).exclude(cfa_mail_id='').count()
        elif self.reminder_type == 'transporter_agreement_renewal':
            return TransporterAgreement.objects.exclude(transporter_mail_id__isnull=True).exclude(transporter_mail_id='').count()
        return 0


class ReminderSchedule(models.Model):
    """Model for scheduling automated email reminders"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]
    
    DAY_OF_WEEK_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    # Schedule Configuration
    reminder = models.ForeignKey(EmailReminder, on_delete=models.CASCADE, related_name='schedules', verbose_name="Email Reminder")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name="Frequency")
    day_of_week = models.IntegerField(choices=DAY_OF_WEEK_CHOICES, null=True, blank=True, verbose_name="Day of Week")
    day_of_month = models.IntegerField(null=True, blank=True, verbose_name="Day of Month")
    time_of_day = models.TimeField(default='09:00', verbose_name="Time of Day")
    
    # Custom Schedule
    custom_days_before_expiry = models.IntegerField(null=True, blank=True, verbose_name="Days Before Expiry")
    custom_days_after_expiry = models.IntegerField(null=True, blank=True, verbose_name="Days After Expiry")
    
    # Status and Control
    is_active = models.BooleanField(default=True, verbose_name="Active")
    last_run = models.DateTimeField(null=True, blank=True, verbose_name="Last Run")
    next_run = models.DateTimeField(null=True, blank=True, verbose_name="Next Run")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='schedules_created')
    
    class Meta:
        verbose_name = "Reminder Schedule"
        verbose_name_plural = "Reminder Schedules"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reminder.name} - {self.get_frequency_display()}"
    
    def calculate_next_run(self):
        """Calculate the next run time based on schedule"""
        now = timezone.now()
        
        if self.frequency == 'daily':
            next_run = now.replace(hour=self.time_of_day.hour, minute=self.time_of_day.minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        
        elif self.frequency == 'weekly' and self.day_of_week is not None:
            days_ahead = self.day_of_week - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            next_run = now.replace(hour=self.time_of_day.hour, minute=self.time_of_day.minute, second=0, microsecond=0) + timedelta(days=days_ahead)
        
        elif self.frequency == 'monthly' and self.day_of_month is not None:
            try:
                next_run = now.replace(day=self.day_of_month, hour=self.time_of_day.hour, minute=self.time_of_day.minute, second=0, microsecond=0)
                if next_run <= now:
                    # Move to next month
                    if now.month == 12:
                        next_run = next_run.replace(year=now.year + 1, month=1)
                    else:
                        next_run = next_run.replace(month=now.month + 1)
            except ValueError:
                # Handle invalid day of month (e.g., 31st in February)
                next_run = now.replace(hour=self.time_of_day.hour, minute=self.time_of_day.minute, second=0, microsecond=0) + timedelta(days=30)
        
        else:
            # Default to daily if no specific schedule
            next_run = now.replace(hour=self.time_of_day.hour, minute=self.time_of_day.minute, second=0, microsecond=0) + timedelta(days=1)
        
        return next_run
    
    def save(self, *args, **kwargs):
        if not self.next_run:
            self.next_run = self.calculate_next_run()
        super().save(*args, **kwargs)


class ReminderLog(models.Model):
    """Model for logging email reminder activities"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
    ]
    
    # Log Information
    schedule = models.ForeignKey(ReminderSchedule, on_delete=models.CASCADE, related_name='logs', verbose_name="Schedule")
    reminder = models.ForeignKey(EmailReminder, on_delete=models.CASCADE, related_name='logs', verbose_name="Reminder")
    
    # Recipient Information
    recipient_email = models.EmailField(verbose_name="Recipient Email")
    recipient_name = models.CharField(max_length=200, verbose_name="Recipient Name")
    record_type = models.CharField(max_length=50, verbose_name="Record Type")
    record_id = models.CharField(max_length=50, verbose_name="Record ID")
    
    # Email Details
    subject = models.CharField(max_length=300, verbose_name="Email Subject")
    message = models.TextField(verbose_name="Email Message")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    
    # Error Information
    error_message = models.TextField(blank=True, verbose_name="Error Message")
    retry_count = models.IntegerField(default=0, verbose_name="Retry Count")
    
    # Timestamps
    scheduled_at = models.DateTimeField(verbose_name="Scheduled At")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Sent At")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Reminder Log"
        verbose_name_plural = "Reminder Logs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.reminder.name} - {self.recipient_email} - {self.get_status_display()}"
    
    def mark_sent(self):
        """Mark the reminder as sent"""
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save()
    
    def mark_failed(self, error_message=""):
        """Mark the reminder as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.retry_count += 1
        self.save()
    
    def mark_skipped(self, reason=""):
        """Mark the reminder as skipped"""
        self.status = 'skipped'
        self.error_message = reason
        self.save()


class ReminderTemplate(models.Model):
    """Model for managing email templates with variables"""
    TEMPLATE_TYPE_CHOICES = [
        ('spo_rent', 'SPO Rent'),
        ('cfa_agreement', 'CFA Agreement'),
        ('transporter_agreement', 'Transporter Agreement'),
        ('payment', 'Payment'),
        ('general', 'General'),
    ]
    
    # Template Information
    name = models.CharField(max_length=200, verbose_name="Template Name")
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPE_CHOICES, verbose_name="Template Type")
    subject = models.CharField(max_length=300, verbose_name="Email Subject")
    body = models.TextField(verbose_name="Email Body")
    
    # Variables
    available_variables = models.TextField(blank=True, verbose_name="Available Variables", 
                                         help_text="List of available variables for this template")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='templates_created')
    
    class Meta:
        verbose_name = "Reminder Template"
        verbose_name_plural = "Reminder Templates"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    def get_variables_list(self):
        """Get list of available variables"""
        if self.available_variables:
            return [var.strip() for var in self.available_variables.split(',')]
        return []
    
    def render_template(self, context_data):
        """Render template with provided context data"""
        try:
            # Simple template rendering - replace variables
            rendered_subject = self.subject
            rendered_body = self.body
            
            for key, value in context_data.items():
                placeholder = f"{{{{{key}}}}}"
                rendered_subject = rendered_subject.replace(placeholder, str(value))
                rendered_body = rendered_body.replace(placeholder, str(value))
            
            return rendered_subject, rendered_body
        except Exception as e:
            return self.subject, f"Error rendering template: {str(e)}"

class ChatbotQuestion(models.Model):
    """Model for storing chatbot questions and their responses"""
    question = models.CharField(max_length=500, help_text="The question to display to users")
    response = models.TextField(help_text="The response to provide when this question is selected")
    category = models.CharField(max_length=100, choices=[
        ('general', 'General'),
        ('spo_rent', 'SPO Rent'),
        ('cfa_agreement', 'CFA Agreement'),
        ('transporter', 'Transporter Agreement'),
        ('approval', 'Approval Process'),
        ('technical', 'Technical Support'),
    ], default='general')
    is_active = models.BooleanField(default=True, help_text="Whether this question is currently available")
    order = models.IntegerField(default=0, help_text="Order in which questions should appear")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'question']
        verbose_name = "Chatbot Question"
        verbose_name_plural = "Chatbot Questions"

    def __str__(self):
        return f"{self.category}: {self.question[:50]}"

class ChatbotSession(models.Model):
    """Model for tracking chatbot conversation sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Chatbot Session"
        verbose_name_plural = "Chatbot Sessions"

    def __str__(self):
        return f"Session {self.session_id} - {self.user.username if self.user else 'Anonymous'}"

class ChatbotMessage(models.Model):
    """Model for storing individual messages in chatbot conversations"""
    session = models.ForeignKey(ChatbotSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=[
        ('user', 'User Message'),
        ('bot', 'Bot Response'),
        ('system', 'System Message'),
    ])
    content = models.TextField()
    question = models.ForeignKey(ChatbotQuestion, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Chatbot Message"
        verbose_name_plural = "Chatbot Messages"

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}"



# Simple User Menu Access Model
class UserMenuAccess(models.Model):
    """Simple model to store user menu access preferences"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='menu_access')
    spo_menu_enabled = models.BooleanField(default=True, verbose_name="SPO Menu Enabled")
    cfa_menu_enabled = models.BooleanField(default=True, verbose_name="CFA Menu Enabled")
    transport_menu_enabled = models.BooleanField(default=True, verbose_name="Transport Menu Enabled")
    approval_menu_enabled = models.BooleanField(default=True, verbose_name="Approval Menu Enabled")
    approval_workflow_enabled = models.BooleanField(default=True, verbose_name="Approval Workflow Enabled")
    report_enabled = models.BooleanField(default=True, verbose_name="Report Enabled")
    mail_reminder_enabled = models.BooleanField(default=True, verbose_name="Mail Reminder Enabled")
    user_management_enabled = models.BooleanField(default=True, verbose_name="User Management Enabled")
    user_menu_access_control_enabled = models.BooleanField(default=True, verbose_name="User Menu Access Control Enabled")
    
    # Legacy fields from old complex system (kept for compatibility)
    can_view = models.BooleanField(default=True)
    can_create = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=True)
    can_delete = models.BooleanField(default=True)
    can_approve = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Menu Access"
        verbose_name_plural = "User Menu Access"

    def __str__(self):
        return f"Menu Access for {self.user.username}"

    def save(self, *args, **kwargs):
        # Ensure all users have menu access by default
        super().save(*args, **kwargs)
