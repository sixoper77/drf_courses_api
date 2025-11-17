from rest_framework import views
from . models import Course
from django.db.models import Avg,Count
from rest_framework.response import Response
from .serializers import (ShortCourseSerializer,UserRegistrationSerializer,UserSerializer,UserLogInSerializer,
                          DetailCourseSerializer,CourseAddSerializer,EnrollmentAddSerializer,ReviewAddSerializer,LessonAddSerializer)
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from rest_framework import views
from .permissions import IsTeacher
from rest_framework.permissions import IsAuthenticated

class ShortCoursesAPIView(views.APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        courses=Course.objects.annotate(
            avg_rating=Avg('reviews__grade')
        ).select_related('teacher')
        serializer=ShortCourseSerializer(courses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class=UserRegistrationSerializer
    permission_classes=[permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        refresh=RefreshToken.for_user(user)
        
        return Response({
            "user":UserSerializer(user).data,
            "refresh":str(refresh),
            "access":str(refresh.access_token),
            "message":"Registration was successful",
            
        },status=status.HTTP_201_CREATED)
        
class UserLogInAPIView(generics.GenericAPIView):
    serializer_class=UserLogInSerializer
    permission_classes=[permissions.AllowAny]
    
    def post(self,request,*args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        
        refresh=RefreshToken.for_user(user)
        
        return Response({
            "user":UserSerializer(user).data,
            "refresh":str(refresh),
            "access":str(refresh.access_token),
            "message":"Login was successful",
            
        },status=status.HTTP_200_OK)
        
class LogOutAPIView(views.APIView):
    permission_classes=[permissions.IsAuthenticated] 
    def post(request):
        refresh_token=request.data.get('refresh_token')
        if refresh_token:
            RefreshToken(refresh_token).blacklist()
            return Response({
                "message":"Logout succesful"
            },status=status.HTTP_200_OK)
        else:
            return Response({
                "message":"Invalid token"
            },status=status.HTTP_400_BAD_REQUEST)
            
class CourseDetailAPIView(views.APIView):
    def get(self,request,pk):
        course=Course.objects.annotate(
            avg_rating=Avg('reviews__grade'),
            students_count=Count('enrollment')
        ).select_related('teacher').prefetch_related('lessons','reviews','reviews__student',).get(pk=pk)
        serializer=DetailCourseSerializer(course)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class CourseCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsTeacher]
    serializer_class=CourseAddSerializer
    
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
        
class EnrollmentCreateAPIView(generics.CreateAPIView):
    serializer_class=EnrollmentAddSerializer
    permission_classes=[IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
        
class ReviewCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=ReviewAddSerializer
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
        
class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes=[IsTeacher]
    serializer_class=LessonAddSerializer
    
    