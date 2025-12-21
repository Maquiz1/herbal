import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from datetime import timedelta
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from nimregenin.models import Demographic, Visit

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Makes automated voice calls for overdue visits using Twilio Voice'

    def handle(self, *args, **options):
        try:
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
            from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)

            if not all([account_sid, auth_token, from_number]):
                self.stderr.write(self.style.ERROR("Twilio credentials missing!"))
                return

            client = Client(account_sid, auth_token)

            today = timezone.now().date()
            grace_period = timedelta(days=7)

            overdue_visits = Visit.objects.filter(
                planned_date__lt=today - grace_period,
                completed=False
            ).select_related('patient')

            if not overdue_visits.exists():
                self.stdout.write(self.style.SUCCESS("No overdue visits. No calls made."))
                return

            # Group by site
            sites_overdue = {}
            for visit in overdue_visits:
                site_code = visit.patient.site or 'UNKNOWN'
                sites_overdue.setdefault(site_code, []).append(visit)

            # Site phone numbers for voice calls
            SITE_VOICE_NUMBERS = {
                'SITE001': ['+15551234567'],  # Coordinator phones
                'SITE002': ['+15551112222'],
                # Add real numbers
            }
            CENTRAL_VOICE_NUMBERS = ['+15550000000']

            total_calls = 0
            total_failed = 0

            base_url = 'https://yourdomain.com'  # CHANGE TO YOUR DOMAIN

            for site_code, visits in sites_overdue.items():
                recipients = SITE_VOICE_NUMBERS.get(site_code, CENTRAL_VOICE_NUMBERS)
                twiml_url = f"{base_url}{reverse('voice_reminder_site', args=[site_code])}"

                for phone in recipients:
                    try:
                        call = client.calls.create(
                            to=phone,
                            from_=from_number,
                            url=twiml_url,
                            method='GET',
                            status_callback=f"{base_url}/voice/status/",  # Optional: log call status
                            status_callback_method='POST'
                        )
                        total_calls += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"Call initiated to {phone} (SID: {call.sid})")
                        )
                        logger.info(f"Voice call to {phone} for site {site_code}")
                    except TwilioRestException as e:
                        total_failed += 1
                        self.stderr.write(self.style.ERROR(f"Call failed to {phone}: {e.msg}"))
                        logger.error(f"Voice call failed: {e}")
                    except Exception as e:
                        total_failed += 1
                        self.stderr.write(self.style.ERROR(f"Unexpected error calling {phone}: {e}"))
                        logger.error(f"Voice call error: {e}")

            summary = f"Voice reminders: {total_calls} initiated"
            if total_failed:
                summary += f", {total_failed} failed"
            self.stdout.write(self.style.SUCCESS(summary))

        except Exception as e:
            logger.critical(f"Critical error in voice reminders: {e}", exc_info=True)
            self.stderr.write(self.style.ERROR(f"Critical failure: {e}"))