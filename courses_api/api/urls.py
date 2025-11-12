from django.urls import path
from . import views
app_name='api'

urlpatterns = [
    path('api/v1/courses/',views.ShortCoursesAPIView.as_view())
]
