from django.conf import settings
from django.db import models


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='courses_teaching',
    )
    credits = models.PositiveIntegerField(default=0)
    capacity = models.PositiveIntegerField(default=30)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code} - {self.name}'


class CourseOffering(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='offerings')
    semester = models.CharField(max_length=20)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text='Override course capacity')

    class Meta:
        ordering = ['semester', 'day_of_week', 'start_time']
        unique_together = [['course', 'semester', 'day_of_week', 'start_time']]

    def __str__(self):
        return f'{self.course.code} {self.semester} {self.get_day_of_week_display()} {self.start_time}'

    @property
    def effective_capacity(self):
        return self.capacity if self.capacity is not None else self.course.capacity
