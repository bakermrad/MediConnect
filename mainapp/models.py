import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import Group

doctor_group, _ = Group.objects.get_or_create(name='Doctor')
nurse_group, _ = Group.objects.get_or_create(name='Nurse')
patient_group, _ = Group.objects.get_or_create(name='Patient')


def send_email_critical_updates(modeladmin, request, queryset):
    for appointment in queryset:
        subject = 'Critical Updates'
        message = f"""
            <html>
                <head>
                    <title>{subject}</title>
                    <style>
                        h1 {{
                            text-align: center;
                            margin-top: 0;
                            margin-bottom: 1rem;
                            color: red;
                        }}
                    </style>
                </head>
                <body>
                    <h1>{subject}</h1>
                    <p>please check the website for the new updates. </p>
                </body>
            </html>
        """
        from_email = 'bakermrad0@django.com'
        recipient_list = [appointment.patient.user.email]
        send_mail(subject, message, from_email, recipient_list, html_message=message)
    modeladmin.message_user(request, f'Successfully sent {queryset.count()} emails.')


send_email_critical_updates.short_description = 'send_email_critical_updates'


def send_email_Appointment_Reminder(modeladmin, request, queryset):
    for appointment in queryset:
        subject = 'Appointment Reminder'
        message = f"""
            <html>
                <head>
                    <title>{subject}</title>
                    <style>
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                            max-width: 600px;
                            margin: 0 auto;
                        }}
                        th, td {{
                            text-align: left;
                            padding: 8px;
                            border-bottom: 1px solid #ddd;
                        }}
                        th {{
                            background-color: #f2f2f2;
                        }}
                        h1 {{
                            text-align: center;
                            margin-top: 0;
                            margin-bottom: 1rem;
                            color: red;
                        }}
                    </style>
                </head>
                <body>
                    <h1>{subject}</h1>
                    <table>
                        <tr>
                            <th>Doctor</th>
                            <td>{appointment.doctor.user.username}</td>
                        </tr>
                        <tr>
                            <th>Patient</th>
                            <td>{appointment.patient.user.username}</td>
                        </tr>
                        <tr>
                            <th>Date</th>
                            <td>{appointment.appoint_date}</td>
                        </tr>
                        <tr>
                            <th>Time</th>
                            <td>{appointment.appoint_time}</td>
                        </tr>
                    </table>
                </body>
            </html>
        """

        from_email = 'bakermrad0@gmail.com'
        recipient_list = [appointment.patient.user.email]
        send_mail(subject, message, from_email, recipient_list, html_message=message)
    
    modeladmin.message_user(request, f'Successfully sent {queryset.count()} emails.')

send_email_Appointment_Reminder.short_description = 'send_email_Appointment_Reminder'

def send_email_important_announcements(modeladmin, request, queryset):
    for appointment in queryset:
        subject = 'Important Announcements'
        message = f"""
            <html>
                <head>
                    <title>{subject}</title>
                    <style>
                        table {{
                            border-collapse: collapse;
                            width: 100%;
                            max-width: 600px;
                            margin: 0 auto;
                        }}
                        th, td {{
                            text-align: left;
                            padding: 8px;
                            border-bottom: 1px solid #ddd;
                        }}
                        th {{
                            background-color: #f2f2f2;
                        }}
                        h1 {{
                            text-align: center;
                            margin-top: 0;
                            margin-bottom: 1rem;
                            color: red;
                        }}
                    </style>
                </head>
                <body>
                    <h1>{subject}</h1>
                    <p>Hi {appointment.patient.user.username}, we have an important anouncements please check your account to learn more.</p>
                </body>
            </html>
        """
        from_email = 'bakermrad0@gmail.com'
        recipient_list = [appointment.patient.user.email]
        send_mail(subject, message, from_email, recipient_list, html_message=message)
    modeladmin.message_user(
        request, f'Successfully sent {queryset.count()} emails.')


send_email_important_announcements.short_description = 'send_email_important_announcements'


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

    @property
    def age(self):
        today = datetime.date.today()
        age = today.year - self.dob.year
        if today < datetime.date(today.year, self.dob.month, self.dob.day):
            age -= 1
        return age


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    appoint_date = models.DateField()
    appoint_time = models.TimeField()
    treatment = models.TextField()

    def __str__(self):
        return f"{self.patient}, {self.doctor}"
