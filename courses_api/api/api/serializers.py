from rest_framework import serializers
from . models import Course,User
from django.db.models import Avg
from django.contrib.auth.password_validation import validate_password
from .validators import CourseUniqueValidator
from django.contrib.auth import authenticate


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
    

class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,
                                   validators=[validate_password])
    password_confirmed=serializers.CharField(write_only=True)
    email=serializers.EmailField(validators=[CourseUniqueValidator(User,"email")])
    username=serializers.CharField(validators=[CourseUniqueValidator(User,"username")])
    is_teacher=serializers.BooleanField(default=False)
    
    class Meta:
        model=User
        fields=('username','first_name','last_name','password','is_teacher','password_confirmed','email')
        
    def validate(self, attrs):
        if attrs['password']!=attrs['password_confirmed']:
            raise serializers.ValidationError({
                "password":"passwords don't match"
            })
        return attrs
    def create(self, validated_data):
        validated_data.pop('password_confirmed')
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name',''),
            password=validated_data['password'],
            is_teacher=validated_data.get('is_teacher',False)
        )
        return user
    
class UserLogInSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    email=serializers.EmailField()
    
    def validate(self, attrs):
        password=attrs.get('password')
        email=attrs.get('email')
        if password and email:
            user=authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError('User not found.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user']=user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password')
    
            
    
    