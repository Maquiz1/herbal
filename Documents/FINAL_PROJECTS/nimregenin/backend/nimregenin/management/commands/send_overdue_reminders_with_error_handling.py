import logging
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta
from nimregenin.models import Demographic, Visit

# Configure logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends per-site email reminders for overdue visits with full error handling'

    def handle(self, *args, **options):
        try:
            today = timezone.now().date()
            grace_period = timedelta(days=7)
            cutoff_date = today - grace_period

            self.stdout.write(f"Checking for overdue visits as of {today} "
                              f"(cutoff: {cutoff_date})...")

            # Fetch overdue visits
            try:
                overdue_visits = Visit.objects.filter(
                    planned_date__lt=cutoff_date,
                    completed=False
                ).select_related('patient').order_by('patient__site', 'patient__patient_id')
            except Exception as e:
                logger.error(f"Database query failed: {e}")
                self.stderr.write(self.style.ERROR(f"Failed to query overdue visits: {e}"))
                return

            if not overdue_visits.exists():
                self.stdout.write(self.style.SUCCESS("No overdue visits found. No emails sent."))
                return

            self.stdout.write(f"Found {overdue_visits.count()} overdue visit(s). Processing...")

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
                    'days_overdue': max(days_overdue, 0)  # Safety
                })

            # Email configuration
            site_emails = getattr(settings, 'SITE_REMINDER_EMAILS', {})
            central_emails = getattr(settings, 'CENTRAL_OVERDUE_RECIPIENTS', [])

            if not site_emails and not central_emails:
                self.stderr.write(self.style.ERROR("No email recipients configured in settings!"))
                logger.error("No recipients configured for overdue reminders")
                return

            total_emails_sent = 0
            total_errors = 0

            for site_code, data in sites_overdue.items():
                recipients = site_emails.get(site_code) or central_emails

                if not recipients:
                    msg = f"No recipients configured for site {site_code} ({data['site_name']})"
                    self.stdout.write(self.style.WARNING(msg))
                    logger.warning(msg)
                    continue

                context = {
                    'today': today,
                    'site_code': site_code,
                    'site_name': data['site_name'],
                    'patients_overdue': data['patients'],
                    'total_overdue': sum(len(p['visits']) for p in data['patients'].values()),
                }

                subject = f"[NIM Regenin] Overdue Visits at {data['site_name']} - {today.strftime('%b %d, %Y')}"

                try:
                    html_message = render_to_string('emails/site_overdue_reminder.html', context)
                    plain_message = render_to_string('emails/site_overdue_reminder.txt', context)
                except Exception as e:
                    logger.error(f"Template rendering failed for site {site_code}: {e}")
                    self.stderr.write(self.style.ERROR(f"Failed to render email for {data['site_name']}: {e}"))
                    total_errors += 1
                    continue

                try:
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
                            f"Sent reminder for {data['site_name']} "
                            f"({context['total_overdue']} visits) to {len(recipients)} recipient(s)"
                        )
                    )
                    logger.info(f"Overdue reminder sent to site {site_code}: {recipients}")
                except Exception as e:
                    total_errors += 1
                    error_msg = f"Failed to send email to {recipients} for site {site_code}: {e}"
                    logger.error(error_msg)
                    self.stderr.write(self.style.ERROR(error_msg))

            # Final summary
            summary = f"Overdue reminder process completed: {total_emails_sent} email(s) sent"
            if total_errors > 0:
                summary += f", {total_errors} error(s)"
                self.stdout.write(self.style.WARNING(summary))
            else:
                self.stdout.write(self.style.SUCCESS(summary))

            logger.info(summary)

        except Exception as e:
            # Catch-all for unexpected crashes
            critical_error = f"Critical error in send_overdue_reminders command: {e}"
            logger.critical(critical_error, exc_info=True)
            self.stderr.write(self.style.ERROR(critical_error))