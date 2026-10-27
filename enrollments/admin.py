from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'offering', 'status', 'enrolled_at', 'dropped_at']
    list_filter = ['status', 'offering__semester']
    search_fields = ['student__username', 'student__email', 'offering__course__code']
    readonly_fields = ['enrolled_at']
