import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from nimregenin.models import Patient, Visit

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends WhatsApp reminders for overdue visits (per-site) using Twilio WhatsApp API'

    def handle(self, *args, **options):
        try:
            # Twilio client
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            from_whatsapp = f"whatsapp:{getattr(settings, 'TWILIO_PHONE_NUMBER', None)}"

            if not all([account_sid, auth_token, from_whatsapp]):
                self.stderr.write(self.style.ERROR("Twilio/WhatsApp credentials missing!"))
                logger.error("Twilio configuration incomplete")
                return

            client = Client(account_sid, auth_token)

            today = timezone.now().date()
            grace_period = timedelta(days=7)
            cutoff_date = today - grace_period

            self.stdout.write(f"Checking overdue visits for WhatsApp alerts as of {today}...")

            overdue_visits = Visit.objects.filter(
                planned_date__lt=cutoff_date,
                completed=False
            ).select_related('patient').order_by('patient__site')

            if not overdue_visits.exists():
                self.stdout.write(self.style.SUCCESS("No overdue visits. No WhatsApp messages sent."))
                return

            # Group by site
            sites_overdue = {}
            for visit in overdue_visits:
                site_code = visit.patient.site or 'UNKNOWN'
                if site_code not in sites_overdue:
                    sites_overdue[site_code] = {
                        'site_name': dict(Patient.SITE_CHOICES).get(site_code, 'Unknown Site'),
                        'visits': []
                    }
                days_overdue = (today - (visit.planned_date + grace_period)).days
                sites_overdue[site_code]['visits'].append({
                    'patient_id': visit.patient.patient_id,
                    'visit_type': visit.get_visit_type_display(),
                    'planned_date': visit.planned_date,
                    'days_overdue': max(days_overdue, 0)
                })

            # WhatsApp recipients
            site_whatsapp = getattr(settings, 'SITE_WHATSAPP_NUMBERS', {})
            central_whatsapp = getattr(settings, 'CENTRAL_WHATSAPP_NUMBERS', [])

            total_sent = 0
            total_failed = 0

            for site_code, data in sites_overdue.items():
                recipients = site_whatsapp.get(site_code) or central_whatsapp

                if not recipients:
                    msg = f"No WhatsApp recipients for site {site_code}"
                    self.stdout.write(self.style.WARNING(msg))
                    logger.warning(msg)
                    continue

                # Build message
                visit_list = "\n".join([
                    f"• {v['patient_id']}: {v['visit_type']} ({v['days_overdue']}d overdue)"
                    for v in data['visits'][:6]
                ])
                if len(data['visits']) > 6:
                    visit_list += f"\n... and {len(data['visits']) - 6} more"

                message_body = (
                    f"*🚨 NIM Regenin Overdue Alert*\n\n"
                    f"*Site:* {data['site_name']}\n"
                    f"*Overdue visits:* {len(data['visits'])}\n\n"
                    f"{visit_list}\n\n"
                    f"Please log in to update: https://yourdomain.com/patients/\n\n"
                    f"_Automated reminder from NIM Regenin EDC_"
                )

                for to_whatsapp in recipients:
                    try:
                        message = client.messages.create(
                            body=message_body,
                            from_=from_whatsapp,
                            to=to_whatsapp
                        )
                        total_sent += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"WhatsApp sent to {to_whatsapp} (SID: {message.sid})")
                        )
                        logger.info(f"WhatsApp sent to {to_whatsapp} for site {site_code}")
                    except TwilioRestException as e:
                        total_failed += 1
                        error_msg = f"WhatsApp failed to {to_whatsapp}: {e.msg} (code: {e.code})"
                        self.stderr.write(self.style.ERROR(error_msg))
                        logger.error(error_msg)
                    except Exception as e:
                        total_failed += 1
                        error_msg = f"Unexpected error sending WhatsApp to {to_whatsapp}: {e}"
                        self.stderr.write(self.style.ERROR(error_msg))
                        logger.error(error_msg)

            # Summary
            summary = f"WhatsApp reminders completed: {total_sent} sent"
            if total_failed:
                summary += f", {total_failed} failed"
            self.stdout.write(self.style.SUCCESS(summary))
            logger.info(summary)

        except Exception as e:
            critical = f"Critical failure in send_overdue_whatsapp: {e}"
            logger.critical(critical, exc_info=True)
            self.stderr.write(self.style.ERROR(critical))