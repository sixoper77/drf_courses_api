from django.contrib import admin
from .models import Course,Lesson,Enrollment,Review


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    readonly_fields=('created_at','updated_at')
    search_fields=('name','description')

