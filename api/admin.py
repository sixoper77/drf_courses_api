from django.contrib import admin
from .models import Course,Lesson,Enrollment,Review


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=('name','teacher','price','is_available','created_at')
    search_fields=('name','description')
    list_filter=('is_available','created_at')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display=('course','duration','created_at')
    ordering=('course',)
    list_filter=('course',)
    
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display=('course__name','student','progress','is_complete','date_enrolled')
    search_fields=('course__name','student__username')
    list_filter=('is_complete','date_enrolled')
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=('student','course','grade','created_at')
    search_fields=('student__username','course__name','review','grade')
    list_filter=('created_at','grade') 