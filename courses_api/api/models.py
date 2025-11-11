from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator,MinValueValidator

class User(AbstractUser):
    is_teacher=models.BooleanField(default=False)
    
    class Meta:
        db_table='users'
    
    def __str__(self):
        return self.get_username()
    
    @property
    def teacher(self):
        return self.is_teacher==True

class Course(models.Model):
    name=models.CharField(max_length=255,verbose_name='Имя курса',null=True,blank=False)
    description=models.CharField(max_length=1024,verbose_name='Описание курса',null=True,blank=True)
    price=models.DecimalField(max_digits=15,decimal_places=2)
    teacher=models.ForeignKey(User,on_delete=models.CASCADE,related_name='courses_teaching')
    created_at=models.DateTimeField(verbose_name='Дата создания',auto_now_add=True)
    updated_at=models.DateTimeField(verbose_name='Обновлен',auto_now=True)
    is_available=models.BooleanField(verbose_name='Доступность',default=True)

    
    
    class Meta:
        ordering=['-created_at']
        indexes=[
            models.Index(fields=['name','description','is_available']),
            models.Index(fields=['price','teacher'])
        ]
        
    def __str__(self):
        return f"{self.name}-{self.teacher.username}-{self.price}"
    

class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='lessons')
    content=models.CharField(max_length=6024,verbose_name='Контент',null=False,blank=False)
    duration=models.DurationField()
    created_at=models.DateTimeField(verbose_name='Дата создания',auto_now_add=True)
    updated_at=models.DateTimeField(verbose_name='Обновлен',auto_now=True)
    
    class Meta:
        ordering=['-created_at']
        
    def __str__(self):
        return "{}-{}".format(self.course_name,self.duration)
    
class Enrollment(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name='enrollment')
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrollment')
    date_enrolled=models.DateTimeField(auto_now_add=True,verbose_name='Дата записи')
    progress=models.FloatField(default=0,verbose_name='Прогресс прохождения')
    is_complete=models.BooleanField(default=False,verbose_name='Курс завершен')
    
    class Meta:
        unique_together=('student','course')
    
    def __str__(self):
        return "{}-{}".format(self.student,self.course)

class Review(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name='students')
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='reviews')
    review=models.CharField(max_length=255,verbose_name='Отзыв')
    grade=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    created_at=models.DateTimeField(verbose_name='Дата создания',auto_now_add=True)
    updated_at=models.DateTimeField(verbose_name='Обновлен',auto_now=True)
    
    class Meta:
        ordering=['-created_at']
    
    def __str__(self):
        return "{}-{}-{}".format(self.student,self.review[:50],self.grade)
    
    