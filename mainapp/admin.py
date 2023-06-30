from django.contrib import admin
from .models import *

class DoctorAdmin(admin.ModelAdmin):
    list_display=['user','specialty','phone','email']


admin.site.register(Doctor,DoctorAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'nurse',
                    'appoint_date', 'appoint_time', 'treatment')
    actions = [send_email_critical_updates,
               send_email_important_announcements, send_email_Appointment_Reminder]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.groups.filter(name='Doctor').exists():
            qs = qs.filter(doctor__user=user)
        else:
            qs = qs.none()

        return qs


admin.site.register(Appointment, AppointmentAdmin)


class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'address', 'phone', 'email', 'age')


admin.site.register(Patient,PatientAdmin)

class NurseAdmin(admin.ModelAdmin):
    list_display=('user', 'phone','email')
admin.site.register(Nurse,NurseAdmin)
