from django.urls import path
from . import views
app_name='api'

urlpatterns = [
    path('api/v1/courses/',views.ShortCoursesAPIView.as_view()),
    path('api/v1/registration/',views.UserRegisterAPIView.as_view()),
    path('api/v1/login/',views.UserLogInAPIView.as_view()),
    path('api/v1/courses/<int:pk>/',views.CourseDetailAPIView.as_view())
]
