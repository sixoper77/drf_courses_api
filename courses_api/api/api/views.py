from rest_framework import views
from . models import Course
from django.db.models import Avg
from rest_framework.response import Response
from .serializers import ShortCourseSerializer,UserRegistrationSerializer,UserSerializer,UserLogInSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.contrib.auth import login
class ShortCoursesAPIView(views.APIView):
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