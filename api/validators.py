from rest_framework import serializers
class CourseUniqueValidator:
    def __init__(self,model,field):
        self.model=model
        self.field=field
    def __call__(self,value):
        custom_kwargs={self.field:value}
        if self.model.objects.filter(**custom_kwargs).exists():
            raise serializers.ValidationError("This {} is already in use.".format(self.field))