# herbal

python manage.py populate_sample_data

python manage.py send_overdue_reminders


# Edit crontab
crontab -e

# Add this line to run daily at 8 AM
0 8 * * * /path/to/your/project/venv/bin/python /path/to/your/project/manage.py send_overdue_reminders >> /path/to/log/overdue_reminders.log 2>&1