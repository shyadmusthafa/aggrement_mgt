#!/usr/bin/env python
"""
Django management command to send scheduled email reminders
Usage: python manage.py send_scheduled_reminders
"""

import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from dashboard.models import (
    ReminderSchedule, ReminderLog, EmailReminder,
    SPORent, CFAAgreement, TransporterAgreement
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send scheduled email reminders based on configured schedules'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force send all pending reminders regardless of schedule',
        )
        parser.add_argument(
            '--schedule-id',
            type=int,
            help='Send reminders for a specific schedule ID only',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting scheduled reminder processing...')
        )
        
        dry_run = options['dry_run']
        force = options['force']
        schedule_id = options['schedule_id']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 DRY RUN MODE - No emails will be sent')
            )
        
        # Get active schedules
        schedules = ReminderSchedule.objects.filter(is_active=True)
        if schedule_id:
            schedules = schedules.filter(id=schedule_id)
        
        if not schedules.exists():
            self.stdout.write(
                self.style.WARNING('⚠️ No active schedules found')
            )
            return
        
        total_processed = 0
        total_sent = 0
        total_failed = 0
        
        for schedule in schedules:
            self.stdout.write(f"\n📅 Processing schedule: {schedule}")
            
            # Check if it's time to run this schedule
            if not force and schedule.next_run and schedule.next_run > timezone.now():
                self.stdout.write(f"⏰ Schedule not due yet. Next run: {schedule.next_run}")
                continue
            
            # Process the schedule
            processed, sent, failed = self.process_schedule(schedule, dry_run)
            total_processed += processed
            total_sent += sent
            total_failed += failed
            
            # Update schedule
            if not dry_run:
                schedule.last_run = timezone.now()
                schedule.next_run = schedule.calculate_next_run()
                schedule.save()
        
        # Summary
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write(self.style.SUCCESS('📊 REMINDER PROCESSING SUMMARY'))
        self.stdout.write(f"{'='*50}")
        self.stdout.write(f"Total processed: {total_processed}")
        self.stdout.write(f"Successfully sent: {total_sent}")
        self.stdout.write(f"Failed: {total_failed}")
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 This was a dry run - no emails were actually sent')
            )

    def process_schedule(self, schedule, dry_run=False):
        """Process a single schedule and send reminders"""
        processed = 0
        sent = 0
        failed = 0
        
        reminder = schedule.reminder
        
        # Get recipients based on reminder type
        recipients = self.get_recipients_for_reminder(reminder, schedule)
        
        if not recipients:
            self.stdout.write(f"⚠️ No recipients found for {reminder.reminder_type}")
            return processed, sent, failed
        
        self.stdout.write(f"📧 Found {len(recipients)} recipients")
        
        for recipient in recipients:
            processed += 1
            
            try:
                # Create log entry
                log_entry = ReminderLog.objects.create(
                    schedule=schedule,
                    reminder=reminder,
                    recipient_email=recipient['email'],
                    recipient_name=recipient['name'],
                    record_type=recipient['record_type'],
                    record_id=recipient['record_id'],
                    subject=recipient['subject'],
                    message=recipient['message'],
                    scheduled_at=timezone.now(),
                )
                
                if dry_run:
                    self.stdout.write(f"🔍 Would send to {recipient['email']}: {recipient['subject']}")
                    log_entry.mark_skipped("Dry run mode")
                    continue
                
                # Send email
                send_mail(
                    subject=recipient['subject'],
                    message=recipient['message'],
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient['email']],
                    fail_silently=False,
                )
                
                # Mark as sent
                log_entry.mark_sent()
                sent += 1
                
                self.stdout.write(f"✅ Sent to {recipient['email']}")
                
            except Exception as e:
                failed += 1
                error_msg = str(e)
                self.stdout.write(f"❌ Failed to send to {recipient['email']}: {error_msg}")
                
                if not dry_run:
                    log_entry.mark_failed(error_msg)
        
        return processed, sent, failed

    def get_recipients_for_reminder(self, reminder, schedule):
        """Get recipients for a specific reminder type"""
        recipients = []
        now = timezone.now().date()
        
        if reminder.reminder_type == 'spo_rent_renewal':
            # Get SPO Rent records expiring soon
            days_before = schedule.custom_days_before_expiry or 30
            expiry_date = now + timedelta(days=days_before)
            
            records = SPORent.objects.filter(
                rental_to_date__lte=expiry_date,
                rental_to_date__gte=now,
                status='Active'
            ).exclude(
                cfa_mail_id__isnull=True
            ).exclude(
                cfa_mail_id=''
            )
            
            for record in records:
                context = self.get_spo_rent_context(record)
                subject, message = self.render_reminder_template(reminder, context)
                
                recipients.append({
                    'email': record.cfa_mail_id,
                    'name': record.owner_name or record.spo_name,
                    'record_type': 'SPO Rent',
                    'record_id': record.spo_code,
                    'subject': subject,
                    'message': message,
                })
        
        elif reminder.reminder_type == 'spo_rent_expiry':
            # Get SPO Rent records that have expired
            days_after = schedule.custom_days_after_expiry or 0
            expiry_date = now - timedelta(days=days_after)
            
            records = SPORent.objects.filter(
                rental_to_date__lte=expiry_date,
                status='Active'
            ).exclude(
                cfa_mail_id__isnull=True
            ).exclude(
                cfa_mail_id=''
            )
            
            for record in records:
                context = self.get_spo_rent_context(record)
                subject, message = self.render_reminder_template(reminder, context)
                
                recipients.append({
                    'email': record.cfa_mail_id,
                    'name': record.owner_name or record.spo_name,
                    'record_type': 'SPO Rent',
                    'record_id': record.spo_code,
                    'subject': subject,
                    'message': message,
                })
        
        elif reminder.reminder_type == 'cfa_agreement_renewal':
            # Get CFA Agreement records expiring soon
            days_before = schedule.custom_days_before_expiry or 30
            expiry_date = now + timedelta(days=days_before)
            
            records = CFAAgreement.objects.filter(
                agreement_to_date__lte=expiry_date,
                agreement_to_date__gte=now,
                status='Active'
            ).exclude(
                cfa_mail_id__isnull=True
            ).exclude(
                cfa_mail_id=''
            )
            
            for record in records:
                context = self.get_cfa_agreement_context(record)
                subject, message = self.render_reminder_template(reminder, context)
                
                recipients.append({
                    'email': record.cfa_mail_id,
                    'name': record.owner_name or record.cfa_name,
                    'record_type': 'CFA Agreement',
                    'record_id': record.cfa_code or record.spo_code,
                    'subject': subject,
                    'message': message,
                })
        
        elif reminder.reminder_type == 'transporter_agreement_renewal':
            # Get Transporter Agreement records expiring soon
            days_before = schedule.custom_days_before_expiry or 30
            expiry_date = now + timedelta(days=days_before)
            
            records = TransporterAgreement.objects.filter(
                agreement_to_date__lte=expiry_date,
                agreement_to_date__gte=now,
                status='Active'
            ).exclude(
                transporter_mail_id__isnull=True
            ).exclude(
                transporter_mail_id=''
            )
            
            for record in records:
                context = self.get_transporter_agreement_context(record)
                subject, message = self.render_reminder_template(reminder, context)
                
                recipients.append({
                    'email': record.transporter_mail_id,
                    'name': record.owner_managing_partner or record.transporter_name,
                    'record_type': 'Transporter Agreement',
                    'record_id': record.transporter_code,
                    'subject': subject,
                    'message': message,
                })
        
        return recipients

    def get_spo_rent_context(self, record):
        """Get context data for SPO Rent record"""
        return {
            'spo_code': record.spo_code,
            'spo_name': record.spo_name,
            'owner_name': record.owner_name or 'Valued Customer',
            'rental_from_date': record.rental_from_date.strftime('%d-%m-%Y') if record.rental_from_date else 'N/A',
            'rental_to_date': record.rental_to_date.strftime('%d-%m-%Y') if record.rental_to_date else 'N/A',
            'rent_pm': f"₹{record.rent_pm}" if record.rent_pm else 'N/A',
            'security_deposit': f"₹{record.security_deposit_paid}" if record.security_deposit_paid else 'N/A',
            'state': record.state.state_name if record.state else 'N/A',
            'branch': record.branch.state_branch_name if record.branch else 'N/A',
            'days_remaining': (record.rental_to_date - timezone.now().date()).days if record.rental_to_date else 0,
        }

    def get_cfa_agreement_context(self, record):
        """Get context data for CFA Agreement record"""
        return {
            'cfa_code': record.cfa_code or record.spo_code,
            'cfa_name': record.cfa_name,
            'owner_name': record.owner_name or 'Valued Customer',
            'agreement_from_date': record.agreement_from_date.strftime('%d-%m-%Y'),
            'agreement_to_date': record.agreement_to_date.strftime('%d-%m-%Y'),
            'security_deposit': f"₹{record.security_deposit_rs}",
            'state': record.state.state_name if record.state else 'N/A',
            'days_remaining': (record.agreement_to_date - timezone.now().date()).days,
        }

    def get_transporter_agreement_context(self, record):
        """Get context data for Transporter Agreement record"""
        return {
            'transporter_code': record.transporter_code,
            'transporter_name': record.transporter_name,
            'owner_name': record.owner_managing_partner or 'Valued Customer',
            'agreement_from_date': record.agreement_from_date.strftime('%d-%m-%Y'),
            'agreement_to_date': record.agreement_to_date.strftime('%d-%m-%Y'),
            'security_deposit': f"₹{record.security_deposit_rs}",
            'state': record.state.state_name if record.state else 'N/A',
            'days_remaining': (record.agreement_to_date - timezone.now().date()).days,
        }

    def render_reminder_template(self, reminder, context):
        """Render reminder template with context data"""
        try:
            # Simple template rendering - replace variables
            subject = reminder.subject_template
            message = reminder.message_template
            
            for key, value in context.items():
                placeholder = f"{{{{{key}}}}}"
                subject = subject.replace(placeholder, str(value))
                message = message.replace(placeholder, str(value))
            
            return subject, message
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            return reminder.subject_template, reminder.message_template 