from rest_framework import serializers
from . models import Course, Enrollment, Lesson, Review,User
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
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields=(
            'content',
            'duration',
            'created_at',
            'updated_at'
        )
        
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields='__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    student=UserSerializer(read_only=True)
    class Meta:
        model=Review
        fields=(
            'student',
            'course',
            'review',
            'grade',
            'created_at',
            'updated_at',
        )
        
class ShortCourseSerializer(serializers.ModelSerializer):
    teacher=UserSerializer(read_only=True)
    average_rating=serializers.SerializerMethodField()
    
    class Meta:
        model=Course
        fields=('name','price','teacher','average_rating')
    
    def get_average_rating(self,obj):
        avg=obj.avg_rating
        return round(avg,2) if avg else 0
    
class DetailCourseSerializer(serializers.ModelSerializer):
    teacher=UserSerializer(read_only=True)
    average_rating=serializers.SerializerMethodField()
    students_count=serializers.SerializerMethodField()
    reviews=ReviewSerializer(many=True,read_only=True)
    lessons=LessonSerializer(many=True,read_only=True)
    
    class Meta:
        model=Course
        fields=('name','price','teacher','average_rating','students_count','reviews','lessons')
        
    def get_average_rating(self,obj):
        avg=obj.avg_rating
        return round(avg,2) if avg else 0
    
    def get_students_count(self,obj):
        return obj.students_count
    
    def get_reviews(self,obj):
        return obj.reviews    

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
    
class UserLogInSerializer(serializers.Serializer):
    password=serializers.CharField(write_only=True)
    username=serializers.CharField()
    
    def validate(self, attrs):
        password=attrs.get('password')
        username=attrs.get('username')
        if password and username:
            user=authenticate(
                request=self.context.get('request'),
                username=username,
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
    
            
    
class CourseAddSerializer(serializers.ModelSerializer):
    is_available=serializers.BooleanField(default=False)
    class Meta:
        model=Course
        fields=(
            'name',
            'description',
            'price',
            'is_available'
        )
        
    def validate_price(self,value):
        if value<=0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value
    
class EnrollmentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields=('course',)
        
    def validate(self, attrs):
        user=self.context['request'].user
        course=attrs['course']
        
        if not course.is_available:
            raise serializers.ValidationError('Course not available')
        
        if Enrollment.objects.filter(student=user,course=course).exists():
            raise serializers.ValidationError('You are already enrolled in the course.')
        
        return attrs