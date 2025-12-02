from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import SPORent, MasState, MasStateBranch, CFAAgreement

# Create your tests here.

class SPORentFilterTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        # Create test data
        self.state = MasState.objects.create(
            state_name='Test State',
            state_code='TS',
            status=1
        )
        
        self.branch = MasStateBranch.objects.create(
            state=self.state,
            state_branch_name='Test Branch',
            state_branch_code='TB001',
            status=1
        )
        
        # Create test SPO Rent records
        self.spo1 = SPORent.objects.create(
            state=self.state,
            branch=self.branch,
            district_code='DIST001',
            spo_code='SPO001',
            spo_name='Test SPO 1',
            stru_grp='Road',
            cfa_status='Active',
            inception_date='2024-01-01',
            owner_name='Test Owner 1',
            status='Active',
            security_deposit_paid=5000.00
        )
        
        self.spo2 = SPORent.objects.create(
            state=self.state,
            branch=self.branch,
            district_code='DIST002',
            spo_code='SPO002',
            spo_name='Another SPO',
            stru_grp='Rail',
            cfa_status='Inactive',
            inception_date='2024-01-01',
            owner_name='Test Owner 2',
            status='Inactive',
            security_deposit_paid=15000.00
        )

    def test_spo_rent_list_view(self):
        """Test that the SPO Rent list view loads correctly"""
        response = self.client.get(reverse('spo_rent_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test SPO 1')
        self.assertContains(response, 'Another SPO')

    def test_spo_name_filter(self):
        """Test filtering by SPO name"""
        response = self.client.get(reverse('spo_rent_list'), {'spo_name': 'Test SPO 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test SPO 1')
        self.assertNotContains(response, 'Another SPO')

    def test_spo_code_filter(self):
        """Test filtering by SPO code"""
        response = self.client.get(reverse('spo_rent_list'), {'spo_code': 'SPO001'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SPO001')
        self.assertNotContains(response, 'SPO002')

    def test_status_filter(self):
        """Test filtering by status"""
        response = self.client.get(reverse('spo_rent_list'), {'rent_status': 'Active'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test SPO 1')
        self.assertNotContains(response, 'Another SPO')

    def test_amount_filter(self):
        """Test filtering by rent amount range"""
        response = self.client.get(reverse('spo_rent_list'), {'rent_amount': '0-5000'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test SPO 1')
        self.assertNotContains(response, 'Another SPO')
        
        response = self.client.get(reverse('spo_rent_list'), {'rent_amount': '10000-20000'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Another SPO')
        self.assertNotContains(response, 'Test SPO 1')

    def test_multiple_filters(self):
        """Test multiple filters applied together"""
        response = self.client.get(reverse('spo_rent_list'), {
            'spo_name': 'Test',
            'rent_status': 'Active'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test SPO 1')
        self.assertNotContains(response, 'Another SPO')


class CFAAgreementDynamicDropdownTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        # Create test data
        self.state = MasState.objects.create(
            state_name='Test State',
            state_code='TS',
            status=1
        )
        
        self.branch = MasStateBranch.objects.create(
            state=self.state,
            state_branch_name='Test Branch',
            state_branch_code='TB001',
            status=1
        )

    def test_load_branches_for_cfa(self):
        """Test loading branches for CFA Agreement form"""
        response = self.client.get(reverse('load_branches_for_cfa'), {'state_id': self.state.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('branches', data)
        self.assertEqual(len(data['branches']), 1)
        self.assertEqual(data['branches'][0]['state_branch_name'], 'Test Branch')

    def test_get_branch_details(self):
        """Test getting branch details for CFA Agreement form"""
        response = self.client.get(reverse('get_branch_details'), {'branch_id': self.branch.id})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('district_code', data)
        self.assertEqual(data['district_code'], 'TB001')

    def test_cfa_agreement_create_view(self):
        """Test that the CFA Agreement create view loads correctly"""
        response = self.client.get(reverse('cfa_agreement_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New CFA Agreement')

    def test_cfa_agreement_create_with_branch(self):
        """Test creating CFA Agreement with branch selection"""
        form_data = {
            'state': self.state.id,
            'district_code': 'TB001',
            'district_name': 'Test District',
            'spo_code': 'SPO001',
            'spo_name': 'Test SPO',
            'cfa_status': 'Active',
            'agreement_renewal': 'Agreement',
            'inception_date': '2024-01-01',
            'agreement_from_date': '2024-01-01',
            'agreement_to_date': '2024-12-31',
            'godown_address': 'Test Address',
            'cfa_code': 'CFA001',
            'cfa_name': 'Test CFA',
            'cfa_address': 'Test CFA Address',
            'owner_name': 'Test Owner',
            'owner_contact_no': '1234567890',
            'cfa_mail_id': 'test@example.com',
            'gst_no': '22AAAAA0000A1Z5',
            'pan_no': 'ABCDE1234F',
            'bank_account_name': 'Test Account',
            'bank_account_no': '1234567890',
            'bank_name': 'Test Bank',
            'bank_branch_name': 'Test Bank Branch',
            'bank_ifsc_code': 'SBIN0001234',
            'destination_code': 'DEST001',
            'security_deposit_rs': '10000.00',
            'security_deposit_doc_ref_dd': 'DD123456',
            'status': 'Active',
        }
        
        response = self.client.post(reverse('cfa_agreement_create'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check if CFA Agreement was created
        cfa = CFAAgreement.objects.filter(cfa_code='CFA001').first()
        self.assertIsNotNone(cfa)
        self.assertEqual(cfa.cfa_name, 'Test CFA')
        self.assertEqual(cfa.district_code, 'TB001')
