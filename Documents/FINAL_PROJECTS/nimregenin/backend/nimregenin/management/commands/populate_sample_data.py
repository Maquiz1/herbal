from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date, timedelta
from nimregenin.models import (
    Patient, Screening, Enrollment, Visit,
    CRF1, CRF2, CRF3, CRF4, CRF5, CRF6, CRF7
)


class Command(BaseCommand):
    help = 'Populates sample data: one complete patient and one incomplete patient'

    def handle(self, *args, **options):
        # Create or get admin user
        user, created = User.objects.get_or_create(username='admin')
        if created:
            user.set_password('admin123')
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write("Created admin user: admin / admin123")

        today = date.today()  # December 21, 2025

        # ===================== PATIENT 1: COMPLETE (PT-006) =====================
        demo1 = Patient.objects.create(
            patient_id='PT-009',
            date_of_birth=date(1980, 3, 10),
            age=45,
            gender='M',
            ethnicity='Caucasian',
            race='White',
            site='SITE002',  # Add this if your Demographic model includes site
        )

        Screening.objects.create(
            patient=demo1,
            screening_date=today - timedelta(days=70),
            screening_status='PASS',
            screened_by=user
        )

        enrollment1 = Enrollment.objects.create(
            patient=demo1,
            enrollment_date=today - timedelta(days=60),
            study_id='NIM-001',
            randomization_number='R001',
            status='RANDOMIZED',
            enrolled_by=user
        )

        baseline_date = enrollment1.enrollment_date

        visit_schedule = [
            ('BASELINE', 0),
            ('DAY7', 7),
            ('DAY14', 14),
            ('DAY30', 30),
            ('DAY60', 60),
            ('DAY90', 90),
            ('DAY120', 120),
        ]

        for visit_type, day_offset in visit_schedule:
            planned = baseline_date + timedelta(days=day_offset)
            actual = planned + timedelta(days=1 if day_offset > 0 else 0)  # slight delay

            visit = Visit.objects.create(
                patient=demo1,
                visit_type=visit_type,
                planned_date=planned,
                actual_date=actual,
                completed=True
            )

            # CRF1 - only for Baseline
            if visit_type == 'BASELINE':
                CRF1.objects.create(
                    visit=visit,
                    visit_date=actual,
                    height_cm=178.5,
                    weight_kg=82.0,
                    bmi=25.8,
                    medical_history="Hypertension diagnosed 5 years ago",
                    concomitant_medications="Lisinopril 10mg daily"
                )

            # CRF7 - only for DAY120 (or DAY90 if early termination)
            if visit_type == 'DAY120':
                CRF7.objects.create(
                    visit=visit,
                    completion_date=actual,
                    early_termination=False,
                    study_completion_status='COMPLETED'
                )

            # Common CRFs for ALL visits
            CRF2.objects.create(
                visit=visit,
                visit_date=actual,
                systolic_bp=125 if day_offset > 0 else 130,
                diastolic_bp=80,
                heart_rate=70,
                physical_exam_findings="Normal findings"
            )

            CRF3.objects.create(
                visit=visit,
                visit_date=actual,
                hemoglobin=14.2,
                wbc=6.5,
                platelets=250000,
                creatinine=0.9,
                alt=25,
                ast=30
            )

            CRF4.objects.create(
                visit=visit,
                visit_date=actual,
                ae_description="None reported",
                severity='MILD',
                serious=False,
                outcome="Resolved"
            )

            CRF5.objects.create(
                visit=visit,
                visit_date=actual,
                medication_name="Metformin",
                dose="500mg BID",
                start_date=baseline_date - timedelta(days=365),
                end_date=None
            )

            CRF6.objects.create(
                visit=visit,
                visit_date=actual,
                primary_endpoint_score=92.5 - (day_offset / 10),
                secondary_endpoint_score=88.0,
                clinician_assessment="Good response to treatment"
            )

        self.stdout.write(self.style.SUCCESS("✓ PT-001 created: FULLY COMPLETE (all visits & CRFs)"))


        # ===================== PATIENT 2: INCOMPLETE (PT-005) =====================
        demo2 = Patient.objects.create(
            patient_id='PT-008',
            date_of_birth=date(1990, 7, 20),
            age=35,
            gender='F',
            ethnicity='Asian',
            race='Asian',
            site='SITE001',  # Add this if your Demographic model includes site
        )

        Screening.objects.create(
            patient=demo2,
            screening_date=today - timedelta(days=35),
            screening_status='PASS',
            screened_by=user
        )

        enrollment2 = Enrollment.objects.create(
            patient=demo2,
            enrollment_date=today - timedelta(days=25),
            study_id='NIM-002',
            randomization_number='R002',
            status='ENROLLED',
            enrolled_by=user
        )

        baseline_date2 = enrollment2.enrollment_date

        # Only partial visits: Baseline, Day7, Day30
        partial_visits = ['BASELINE', 'DAY7', 'DAY30']

        for visit_type in partial_visits:
            day_offset = 0 if visit_type == 'BASELINE' else int(visit_type.replace('DAY', ''))
            planned = baseline_date2 + timedelta(days=day_offset)
            actual = planned if visit_type in ['BASELINE', 'DAY7'] else None

            visit = Visit.objects.create(
                patient=demo2,
                visit_type=visit_type,
                planned_date=planned,
                actual_date=actual,
                completed=(actual is not None)
            )

            if visit_type == 'BASELINE':
                CRF1.objects.create(
                    visit=visit,
                    visit_date=actual,
                    height_cm=162.0,
                    weight_kg=58.0,
                    bmi=22.1,
                    medical_history="No significant history",
                    concomitant_medications="None"
                )
                CRF2.objects.create(visit=visit, visit_date=actual, systolic_bp=115, diastolic_bp=75, heart_rate=68)
                CRF3.objects.create(visit=visit, visit_date=actual, hemoglobin=13.0)
                CRF6.objects.create(visit=visit, visit_date=actual, primary_endpoint_score=90.0)

            if visit_type == 'DAY7':
                CRF2.objects.create(visit=visit, visit_date=actual, systolic_bp=118, diastolic_bp=76, heart_rate=70)
                CRF6.objects.create(visit=visit, visit_date=actual, primary_endpoint_score=89.5)

            if visit_type == 'DAY30':
                # Only partial data
                CRF2.objects.create(visit=visit, visit_date=None, systolic_bp=120, diastolic_bp=78, heart_rate=72)

        self.stdout.write(self.style.SUCCESS("✓ PT-002 created: INCOMPLETE (missing visits and CRFs)"))

        self.stdout.write(self.style.SUCCESS("\nSample data populated successfully!"))
        self.stdout.write("→ View patients: http://127.0.0.1:8000/patients/")
        self.stdout.write("→ Admin login: http://127.0.0.1:8000/admin/ (admin / admin123)")