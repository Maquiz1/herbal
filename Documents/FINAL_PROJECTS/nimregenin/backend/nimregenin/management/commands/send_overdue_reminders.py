from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta
from nimregenin.models import Patient, Visit


class Command(BaseCommand):
    help = 'Sends email reminder for overdue visits (past planned date + 7 days, not completed)'

    def handle(self, *args, **options):
        today = timezone.now().date()
        grace_period = timedelta(days=7)
        cutoff_date = today - grace_period

        overdue_visits = Visit.objects.filter(
            planned_date__lt=cutoff_date,
            completed=False,
            actual_date__isnull=True  # Optional: only if visit hasn't occurred
        ).select_related('patient').order_by('patient__patient_id', 'planned_date')

        if not overdue_visits.exists():
            self.stdout.write("No overdue visits today. No email sent.")
            return

        # Group by patient
        patients_overdue = {}
        for visit in overdue_visits:
            pid = visit.patient.patient_id
            if pid not in patients_overdue:
                patients_overdue[pid] = {
                    'patient': visit.patient,
                    'visits': []
                }
            days_overdue = (today - (visit.planned_date + grace_period)).days
            patients_overdue[pid]['visits'].append({
                'visit': visit,
                'days_overdue': days_overdue
            })

        # Render email template
        context = {
            'today': today,
            'patients_overdue': patients_overdue,
            'total_overdue': overdue_visits.count(),
        }

        subject = f"[NIM Regenin] Overdue Visit Reminder - {today.strftime('%B %d, %Y')}"
        html_message = render_to_string('emails/overdue_reminder.html', context)
        plain_message = render_to_string('emails/overdue_reminder.txt', context)

        recipients = getattr(settings, 'OVERDUE_REMINDER_RECIPIENTS', [])
        if not recipients:
            self.stdout.write(self.style.WARNING("No recipients configured in OVERDUE_REMINDER_RECIPIENTS"))
            return

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=recipients,
            html_message=html_message,
            fail_silently=False,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Overdue reminder email sent to {len(recipients)} recipient(s) "
                f"for {overdue_visits.count()} overdue visit(s)"
            )
        )