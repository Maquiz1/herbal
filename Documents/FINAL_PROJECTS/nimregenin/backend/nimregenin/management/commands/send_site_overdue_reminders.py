from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta
from nimregenin.models import Demographic, Visit


class Command(BaseCommand):
    help = 'Sends per-site email reminders for overdue visits'

    def handle(self, *args, **options):
        today = timezone.now().date()
        grace_period = timedelta(days=7)
        cutoff_date = today - grace_period

        overdue_visits = Visit.objects.filter(
            planned_date__lt=cutoff_date,
            completed=False
        ).select_related('patient').order_by('patient__site', 'patient__patient_id')

        if not overdue_visits.exists():
            self.stdout.write("No overdue visits today. No emails sent.")
            return

        # Group by site
        sites_overdue = {}
        for visit in overdue_visits:
            site_code = visit.patient.site or 'UNKNOWN'
            if site_code not in sites_overdue:
                sites_overdue[site_code] = {
                    'site_name': dict(Demographic.SITE_CHOICES).get(site_code, 'Unknown Site'),
                    'patients': {}
                }

            pid = visit.patient.patient_id
            if pid not in sites_overdue[site_code]['patients']:
                sites_overdue[site_code]['patients'][pid] = {
                    'patient': visit.patient,
                    'visits': []
                }

            days_overdue = (today - (visit.planned_date + grace_period)).days
            sites_overdue[site_code]['patients'][pid]['visits'].append({
                'visit': visit,
                'days_overdue': days_overdue
            })

        # Get site email mapping
        site_emails = getattr(settings, 'SITE_REMINDER_EMAILS', {})
        central_emails = getattr(settings, 'CENTRAL_OVERDUE_RECIPIENTS', [])

        total_emails_sent = 0

        for site_code, data in sites_overdue.items():
            recipients = site_emails.get(site_code, central_emails)  # Fallback to central

            if not recipients:
                self.stdout.write(self.style.WARNING(f"No recipients for site {site_code}"))
                continue

            context = {
                'today': today,
                'site_code': site_code,
                'site_name': data['site_name'],
                'patients_overdue': data['patients'],
                'total_overdue': sum(len(p['visits']) for p in data['patients'].values()),
            }

            subject = f"[NIM Regenin] Overdue Visits at {data['site_name']} - {today.strftime('%b %d, %Y')}"
            html_message = render_to_string('emails/site_overdue_reminder.html', context)
            plain_message = render_to_string('emails/site_overdue_reminder.txt', context)

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=None,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False,
            )

            total_emails_sent += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Sent reminder for {data['site_name']} ({context['total_overdue']} visits) "
                    f"to {len(recipients)} recipient(s)"
                )
            )

        self.stdout.write(self.style.SUCCESS(f"\nPer-site reminders completed: {total_emails_sent} email(s) sent"))