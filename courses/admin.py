from django.contrib import admin
from .models import Course, CourseOffering


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'teacher', 'credits', 'capacity']
    list_filter = ['credits']
    search_fields = ['code', 'name']


@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ['course', 'semester', 'day_of_week', 'start_time', 'end_time', 'room', 'effective_capacity']
    list_filter = ['semester', 'day_of_week']
    search_fields = ['course__code', 'course__name']
    readonly_fields = []
