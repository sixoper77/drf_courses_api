from rest_framework import serializers
from . models import Course,User
from django.db.models import Avg


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username',
                'first_name',
                'last_name',
                'id')


class ShortCourseSerializer(serializers.ModelSerializer):
    teacher=UserSerializer(read_only=True)
    average_rating=serializers.SerializerMethodField()
    
    class Meta:
        model=Course
        fields=('name','price','teacher','average_rating')
    
    def get_average_rating(self,obj):
        avg=obj.avg_rating
        return round(avg,2) if avg else 0