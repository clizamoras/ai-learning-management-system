from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = '__all__'

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = '__all__'  

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = '__all__'

class RegisterForm(UserCreationForm):

    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('teacher', 'Teacher')]
    )

    dept = forms.CharField()
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    sem = forms.CharField(required=False)
    yof = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'role',
            'dept',
            'sem',
            'dob',
            'yof'
        ]