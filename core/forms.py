from django import forms
from .models import StudentProfile, TeacherProfile,Course,Lesson,Assignment,Submission,Quiz,Question,Progress

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
class Progress(forms.ModelForm):
    class Meta:
        model=Progress
        fields='__all__'