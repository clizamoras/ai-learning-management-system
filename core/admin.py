from django.contrib import admin
from .models import StudentProfile, TeacherProfile, Course, Enrollment, Lesson, Assignment, Quiz, Question, Option, Submission,Announcements,Progress,Result

admin.site.register(StudentProfile)

# Register your models here.
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Lesson)
admin.site.register(Assignment)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Announcements)
admin.site.register(Progress)
admin.site.register(Result)