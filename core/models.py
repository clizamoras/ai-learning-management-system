from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StudentProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    dept=models.CharField(max_length=200)
    sem=models.CharField(max_length=200)
    dob=models.DateField()

class TeacherProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    dept=models.CharField(max_length=200)
    dob=models.DateField()
    yof=models.IntegerField()

class Course(models.Model):
    name=models.CharField(max_length=200)
    code=models.CharField(max_length=200)
    teacher=models.ForeignKey(TeacherProfile,on_delete=models.CASCADE)

class Enrollment(models.Model):
    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    enrolled_date=models.DateField(auto_now_add=True)

class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    video=models.FileField(upload_to='videos/')
    notes=models.FileField(upload_to='notes/')


class Assignment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    duedate=models.DateField()

class Quiz(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    duedate=models.DateField()

class Question(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question=models.TextField()
    marks=models.IntegerField()

class Option(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    option_text=models.CharField(max_length=200)
    is_correct=models.BooleanField(default=False)

class Submission(models.Model):
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    submitteddate=models.DateField(auto_now_add=True)
    file=models.FileField(upload_to='submissions/')
    marks=models.IntegerField(null=True,blank=True)

class Announcements(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.TextField()
    date=models.DateField(auto_now_add=True)

class Progress(models.Model):
    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)

    progresspercenatge=models.FloatField()
    last_accessed=models.DateField(auto_now=True)
    completedlesson=models.IntegerField()

class Result(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    score=models.IntegerField()
    attempted_date=models.DateTimeField(auto_now_add=True)
