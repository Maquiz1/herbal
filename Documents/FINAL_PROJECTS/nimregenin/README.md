# herbal

python manage.py populate_sample_data

python manage.py send_overdue_reminders

python manage.py send_overdue_reminders

# Edit crontab
crontab -e

# Add this line to run daily at 8 AM
0 8 * * * /path/to/your/project/venv/bin/python /path/to/your/project/manage.py send_overdue_reminders >> /path/to/log/overdue_reminders.log 2>&1



# Send SMS after email reminder
0 9 * * * /path/to/venv/bin/python /path/to/project/manage.py send_overdue_sms >> /path/to/logs/sms_reminders.log 2>&1


0 10 * * * /path/to/venv/bin/python /path/to/project/manage.py send_overdue_whatsapp >> /path/to/logs/whatsapp_reminders.log 2>&1


30 9 * * * /path/to/venv/bin/python /path/to/project/manage.py send_overdue_voice_calls >> /path/to/logs/voice_calls.log 2>&1