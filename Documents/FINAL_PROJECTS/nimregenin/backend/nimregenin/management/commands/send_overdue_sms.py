import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from nimregenin.models import Demographic, Visit

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends SMS reminders for overdue visits (per-site) using Twilio'

    def handle(self, *args, **options):
        try:
            # Initialize Twilio client
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)

            if not all([account_sid, auth_token, from_number]):
                self.stderr.write(self.style.ERROR("Twilio credentials missing in settings!"))
                logger.error("Twilio configuration incomplete")
                return

            client = Client(account_sid, auth_token)

            today = timezone.now().date()
            grace_period = timedelta(days=7)
            cutoff_date = today - grace_period

            self.stdout.write(f"Checking overdue visits as of {today}...")

            overdue_visits = Visit.objects.filter(
                planned_date__lt=cutoff_date,
                completed=False
            ).select_related('patient').order_by('patient__site')

            if not overdue_visits.exists():
                self.stdout.write(self.style.SUCCESS("No overdue visits. No SMS sent."))
                return

            # Group by site
            sites_overdue = {}
            for visit in overdue_visits:
                site_code = visit.patient.site or 'UNKNOWN'
                if site_code not in sites_overdue:
                    sites_overdue[site_code] = {
                        'site_name': dict(Demographic.SITE_CHOICES).get(site_code, 'Unknown Site'),
                        'visits': []
                    }
                days_overdue = (today - (visit.planned_date + grace_period)).days
                sites_overdue[site_code]['visits'].append({
                    'patient_id': visit.patient.patient_id,
                    'visit_type': visit.get_visit_type_display(),
                    'planned_date': visit.planned_date,
                    'days_overdue': max(days_overdue, 0)
                })

            # SMS recipient mapping
            site_sms = getattr(settings, 'SITE_SMS_NUMBERS', {})
            central_sms = getattr(settings, 'CENTRAL_SMS_NUMBERS', [])

            total_sent = 0
            total_failed = 0

            for site_code, data in sites_overdue.items():
                recipients = site_sms.get(site_code) or central_sms

                if not recipients:
                    msg = f"No SMS recipients for site {site_code}"
                    self.stdout.write(self.style.WARNING(msg))
                    logger.warning(msg)
                    continue

                # Build concise message
                visit_list = "\n".join([
                    f"• {v['patient_id']}: {v['visit_type']} ({v['days_overdue']}d overdue)"
                    for v in data['visits'][:5]  # Limit to avoid SMS length issues
                ])
                if len(data['visits']) > 5:
                    visit_list += f"\n... and {len(data['visits']) - 5} more"

                message_body = (
                    f"🚨 NIM Regenin Overdue Alert\n"
                    f"Site: {data['site_name']}\n"
                    f"{len(data['visits'])} overdue visit(s):\n\n"
                    f"{visit_list}\n\n"
                    f"Please log in to resolve: https://yourdomain.com/patients/"
                )

                for phone in recipients:
                    try:
                        message = client.messages.create(
                            body=message_body,
                            from_=from_number,
                            to=phone
                        )
                        total_sent += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"SMS sent to {phone} (SID: {message.sid})")
                        )
                        logger.info(f"SMS sent to {phone} for site {site_code}")
                    except TwilioRestException as e:
                        total_failed += 1
                        error_msg = f"SMS failed to {phone}: {e.msg} (code: {e.code})"
                        self.stderr.write(self.style.ERROR(error_msg))
                        logger.error(error_msg)
                    except Exception as e:
                        total_failed += 1
                        error_msg = f"Unexpected error sending SMS to {phone}: {e}"
                        self.stderr.write(self.style.ERROR(error_msg))
                        logger.error(error_msg)

            # Summary
            summary = f"SMS reminders completed: {total_sent} sent"
            if total_failed:
                summary += f", {total_failed} failed"
            self.stdout.write(self.style.SUCCESS(summary))
            logger.info(summary)

        except Exception as e:
            critical = f"Critical failure in send_overdue_sms: {e}"
            logger.critical(critical, exc_info=True)
            self.stderr.write(self.style.ERROR(critical))