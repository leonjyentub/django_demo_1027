from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import CourseOffering, Course
from enrollments.models import Enrollment


def offering_list(request):
    semester = request.GET.get('semester')
    offerings = CourseOffering.objects.select_related('course', 'course__teacher')
    if semester:
        offerings = offerings.filter(semester=semester)
    return render(request, 'courses/offering_list.html', {'offerings': offerings, 'semester': semester})


@login_required
def enroll(request, offering_id):
    offering = get_object_or_404(CourseOffering, pk=offering_id)
    if getattr(request.user, 'role', None) != 'student':
        messages.error(request, 'Only students can enroll.')
        return redirect('offering_list')

    if Enrollment.objects.filter(student=request.user, offering=offering, status='enrolled').exists():
        messages.warning(request, 'Already enrolled in this offering.')
        return redirect('offering_list')

    enrolled_count = Enrollment.objects.filter(offering=offering, status='enrolled').count()
    if enrolled_count >= offering.effective_capacity:
        messages.error(request, 'Course is full.')
        return redirect('offering_list')

    Enrollment.objects.create(student=request.user, offering=offering, status='enrolled')
    messages.success(request, 'Enrolled successfully.')
    return redirect('my_timetable')


@login_required
def drop(request, offering_id):
    offering = get_object_or_404(CourseOffering, pk=offering_id)
    if getattr(request.user, 'role', None) != 'student':
        messages.error(request, 'Only students can drop courses.')
        return redirect('my_timetable')

    enrollment = Enrollment.objects.filter(student=request.user, offering=offering, status='enrolled').first()
    if not enrollment:
        messages.warning(request, 'You are not enrolled in this offering.')
        return redirect('my_timetable')

    enrollment.status = 'dropped'
    enrollment.dropped_at = timezone.now()
    enrollment.save()
    messages.success(request, 'Dropped successfully.')
    return redirect('my_timetable')


@login_required
def my_timetable(request):
    if getattr(request.user, 'role', None) != 'student':
        messages.error(request, 'Only students can view their timetable.')
        return redirect('offering_list')

    enrollments = (
        Enrollment.objects.filter(student=request.user, status='enrolled')
        .select_related('offering', 'offering__course', 'offering__course__teacher')
        .order_by('offering__day_of_week', 'offering__start_time')
    )

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    timetable = {i: [] for i in range(7)}
    for e in enrollments:
        timetable[e.offering.day_of_week].append(e)

    return render(request, 'courses/timetable.html', {'timetable': timetable, 'days': days, 'enrollments': enrollments})


@login_required
def teacher_dashboard(request):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, '僅教師可使用此功能。')
        return redirect('offering_list')

    courses = Course.objects.filter(teacher=request.user).prefetch_related('offerings')
    offerings = CourseOffering.objects.filter(course__teacher=request.user).select_related('course')
    return render(request, 'courses/teacher_dashboard.html', {'courses': courses, 'offerings': offerings})


@login_required
def teacher_offering_students(request, offering_id):
    if getattr(request.user, 'role', None) != 'teacher':
        messages.error(request, '僅教師可使用此功能。')
        return redirect('offering_list')

    offering = get_object_or_404(CourseOffering, pk=offering_id, course__teacher=request.user)
    enrollments = Enrollment.objects.filter(offering=offering, status='enrolled').select_related('student')
    return render(request, 'courses/teacher_offering_students.html', {'offering': offering, 'enrollments': enrollments})


