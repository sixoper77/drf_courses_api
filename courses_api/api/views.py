from django.shortcuts import render
from rest_framework import views
from . models import Course
from django.db.models import Avg
from rest_framework.response import Response
from .serializers import ShortCourseSerializer
from rest_framework import status

class ShortCoursesAPIView(views.APIView):
    def get(self):
        courses=Course.objects.annotate(
            avg_rating=Avg('reviews__grade')
        ).select_related('teacher')
        serializer=ShortCourseSerializer(courses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
