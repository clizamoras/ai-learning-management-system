from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id','name','code','teacher']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields=['id','course','title','video','notes']

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Assignment
        fields=['id','course','title','description','duedate']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model=Quiz
        fields=['id','course','title','duedate']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['id','quiz','question','marks']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields=['id','question','option_text','is_correct']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields=['id','course','enrolled_date']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=Result
        fields=['id','quiz','score','attempted_date']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Progress
        fields=['id','course','progresspercenatge','last_accessed','completedlesson']