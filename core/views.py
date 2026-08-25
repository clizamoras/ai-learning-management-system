from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.views import View
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import *
import ollama
from .forms import *

# Create your views here.
class Login(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        if hasattr(self.request.user, 'teacherprofile'):
            return reverse_lazy('TeacherDashBoard')
        else:
            return reverse_lazy('StudentDashBoard')
    
class Logout(LogoutView):
    next_page='login'

class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        if form.cleaned_data['role'] == 'student':
            StudentProfile.objects.create(
                user=user,
                dept=form.cleaned_data['dept'],
                sem=form.cleaned_data['sem'],
                dob=form.cleaned_data['dob']
            )
        else:
            TeacherProfile.objects.create(
                user=user,
                dept=form.cleaned_data['dept'],
                dob=form.cleaned_data['dob'],
                yof=form.cleaned_data['yof']
            )

        return super().form_valid(form)

class TeacherDashBoard(LoginRequiredMixin,ListView):
    template_name='teacher.html'
    model=Course
    context_object_name='courses'

    def get_queryset(self):
        return Course.objects.filter(teacher__user=self.request.user)

class CreateCourse(CreateView): 
    model=Course
    template_name='course.html'
    fields=['name','code']
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self,form):  # it is used to make the teacher fixed (only user)
        form.instance.teacher=self.request.user.teacherprofile
        return super().form_valid(form)
            

class CreateLesson(CreateView):
    model=Lesson
    template_name='lesson.html'  
    fields=['course','title','video','notes']
    success_url=reverse_lazy('TeacherDashBoard')
  

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class =None):  # makes sure the teacher can only see their courses not al the courses
        form=super().get_form(form_class)
        form.fields['course'].queryset=Course.objects.filter(teacher__user=self.request.user)
        return form

class CreateAssignment(CreateView):
    model=Assignment
    template_name='assignment.html'
    fields=['course','title','description','duedate']
    success_url=reverse_lazy('TeacherDashBoard')
    

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class = None):
        form= super().get_form(form_class)
        form.fields['course'].queryset=Course.objects.filter(teacher__user=self.request.user)
        return form

class CreateQuiz(CreateView):
    model=Quiz
    template_name='quiz.html'
    fields=['course','title','duedate']
    success_url=reverse_lazy('TeacherDashBoard')
    

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class = None):
        form= super().get_form(form_class)
        form.fields['course'].queryset=Course.objects.filter(teacher__user=self.request.user)
        return form

class StudentSubmission(ListView):
    template_name='submission.html'
    model=Submission
    context_object_name='submissions'

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Submission.objects.filter(assignment__course__teacher__user=self.request.user)
       
class GiveMarks(View):# the teacher is viewing the assignment so in that we are add marks since it is a mixture of list and create we have to use a seperate class
    def post(self, request, pk):
        submission = Submission.objects.get(id=pk)

        submission.marks = request.POST.get('marks')
        submission.save()

        return redirect('/studentsubmission/')

class ViewSubmission(ListView):
    model=Submission
    template_name='subassignments'
    context_object_name='viewassigns'
    def get_queryset(self):
        return Submission.objects.filter(student__user=self.request.user)
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user,'studentprofile'):
            return redirect('TeacherDashBoard')
        return super().dispatch(request, *args, **kwargs)
class CreateQuestion(CreateView):
    template_name='question.html'
    model=Question
    fields=['quiz','question','marks']
    success_url=reverse_lazy('TeacherDashBoard')
    

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class = None):
        form= super().get_form(form_class)
        form.fields['quiz'].queryset=Quiz.objects.filter(course__teacher__user=self.request.user)
        return form
    
    
class CreateOPtion(CreateView):
    model=Option
    template_name='option.html'
    fields=['question','option_text','is_correct']
    success_url=reverse_lazy('TeacherDashBoard')
    

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class = None):
        form= super().get_form(form_class)
        form.fields['question'].queryset=Question.objects.filter(quiz__course__teacher__user=self.request.user)
        return form

class CreateAnnouncement(CreateView):
    model=Announcements
    template_name='announcements.html'
    fields=['course','title','content']
    success_url=reverse_lazy('TeacherDashBoard')
    

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_form(self, form_class = None):
        form=super().get_form(form_class)
        form.fields['course'].queryset=Course.objects.filter(teacher__user=self.request.user)
        return form

class TeacherProgress(CreateView):
    template_name = 'progress.html'
    model = Progress
    fields = ['student', 'course', 'progresspercenatge', 'completedlesson']
    success_url = reverse_lazy('TeacherDashBoard')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['course'].queryset = Course.objects.filter(
            teacher__user=self.request.user
        )
        return form

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
   




class StudentDashBoard(LoginRequiredMixin,ListView):
    model=Course
    template_name='student.html'
    context_object_name='courses'
    def get_queryset(self):
        return Course.objects.filter(enrollment__student__user=self.request.user)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['quizzes']=Quiz.objects.filter(course__enrollment__student__user=self.request.user)
        context['announcements']=Announcements.objects.filter(course__enrollment__student__user=self.request.user)
        context['subassigns']=Submission.objects.filter(student__user=self.request.user)
        return context


class ViewAnnouncement(ListView):
    template_name='viewannouncement.html'
    model=Announcements
    context_object_name='announcements'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user,'studentprofile'):
            return redirect('TeacherDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Announcements.objects.filter(course__enrollment__student__user=self.request.user)
class ViewLesson(ListView):
    model=Lesson
    template_name='lesson_list.html'
    context_object_name='lessons'

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'studentprofile'):
            return redirect('TeacherDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Lesson.objects.filter(course__enrollment__student__user=self.request.user)

class SubmitAssignment(CreateView):
    model=Submission
    template_name='subassign.html'
    fields=['assignment','file']
    success_url=reverse_lazy('StudentDashBoard')
    

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'studentprofile'):
            return redirect('TeacherDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self,form):
        form.instance.student=self.request.user.studentprofile
        return super().form_valid(form)

    def get_form(self, form_class = None):
        form= super().get_form(form_class)
        form.fields['assignment'].queryset=Assignment.objects.filter(course__enrollment__student__user=self.request.user)
        return form

class ViewQuiz(ListView):
    model=Quiz
    template_name="viewquiz.html"
    context_object_name='quizes'

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'studentprofile'):
            return redirect('TeacherDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Quiz.objects.filter(course__enrollment__student__user=self.request.user)

class AttemptQuiz(View):
    def get(self,request,pk):
        questions=Question.objects.filter(quiz_id=pk)
        return render(request,'attempt.html',{"questions":questions})
    def post(self,request,pk):
        quiz=Quiz.objects.get(id=pk)
        score=0
        questions=Question.objects.filter(quiz_id=pk)
        for question in questions:
            answer=request.POST.get(f"question_{question.id}")
            if answer:
                option=Option.objects.get(id=answer)

                if option.is_correct:
                    score +=1
        Result.objects.create(
            quiz=quiz,
            student=self.request.user.studentprofile,
            score=score
        )
        return redirect('ViewResult')
    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'studentprofile'):
            return redirect('TeacherDashBoard')
        return super().dispatch(request, *args, **kwargs)

class ViewProgress(ListView):
    model = Progress
    template_name = 'pro.html'
    context_object_name = 'progresses'

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'studentprofile'):
            return redirect('TeacherDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Progress.objects.filter(student__user=self.request.user)

class CourseDetail(DetailView):
    model=Course
    template_name='coursedetail.html'
    context_object_name='course'
    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        context['lessons']=Lesson.objects.filter(course=self.object)
        context['assignments']=Assignment.objects.filter(course=self.object)
        context['quizes']=Quiz.objects.filter(course=self.object)
        context['announcements']=Announcements.objects.filter(course=self.object)
        return context
class CreateEnrollement(CreateView):
    model=Enrollment
    template_name='enroll.html'
    fields=['course']
    success_url=reverse_lazy('StudentDashBoard')
    
    def form_valid(self,form):
        form.instance.student=self.request.user.studentprofile
        return super().form_valid(form)

    def get_form(self, form_class =None):
        form= super().get_form(form_class)
        form.fields['course'].queryset=Course.objects.exclude(enrollment__student=self.request.user.studentprofile)
        return form
        

class ViewResult(ListView):
    model=Result
    template_name='result.html'
    context_object_name='results'
    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'studentprofile'):
            return redirect('TeacherDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Result.objects.filter(student__user=self.request.user)

class UpdateCourse(UpdateView):
    model=Course
    template_name='updatecourse.html'
    fields=['name','code']
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self): # which courses u want to update
        return Course.objects.filter(teacher__user=self.request.user)

class DeleteCourse(DeleteView):
    model=Course
    template_name='deletecourse.html'
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self): # which courses u want to delete
        return Course.objects.filter(teacher__user=self.request.user)

class UpdateAssignment(UpdateView):
    model=Assignment
    template_name='updateassignment.html'
    fields=['title','description','duedate']
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Assignment.objects.filter(course__teacher__user=self.request.user)

class DeleteAssignment(DeleteView):
    model=Assignment
    template_name='deleteassignment.html'
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Assignment.objects.filter(course__teacher__user=self.request.user)
    

class DeleteLesson(DeleteView):
    model=Lesson
    template_name='deletelesson.html'
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Lesson.objects.filter(course__teacher__user=self.request.user)
    

class UpdateLesson(UpdateView):
    model=Lesson
    template_name='updatelesson.html'
    fields=['title','video','notes']
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Lesson.objects.filter(course__teacher__user=self.request.user)

class DeleteQuiz(DeleteView):
    model=Quiz
    template_name='deletequiz.html'
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Quiz.objects.filter(course__teacher__user=self.request.user)

class UpdateQuiz(UpdateView):
    model=Quiz
    template_name='updatequiz.html'
    fields=['title','duedate']
    success_url=reverse_lazy('TeacherDashBoard')

    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Quiz.objects.filter(course__teacher__user=self.request.user)

class DeleteAnnouncement(DeleteView):
    model=Announcements
    template_name='deleteannouncement.html'
    success_url=reverse_lazy('TeacherDashBoard')
    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Announcements.objects.filter(course__teacher__user=self.request.user)
class UpdateAnnouncement(UpdateView):
    model=Announcements
    template_name='updateannouncement.html'
    fields=['title','content']
    success_url=reverse_lazy('TeacherDashBoard')
    def dispatch(self,request,*args,**kwargs):
        if not hasattr(request.user,'teacherprofile'):
            return redirect('StudentDashBoard')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        return Announcements.objects.filter(course__teacher__user=self.request.user)

class CourseAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None):
        if pk:
            if hasattr(request.user,'teacherprofile'):
                course=Course.objects.get(id=pk,teacher__user=request.user)
            else:
                course=Course.objects.get(id=pk,enrollment__student__user=request.user)
            serializer=CourseSerializer(course)
            return Response(serializer.data)

        if hasattr(request.user,'teacherprofile'):
            course=Course.objects.filter(teacher__user=request.user)
        else:
            course=Course.objects.filter(enrollment__student__user=request.user)
        serializer=CourseSerializer(course,many=True)
        return Response(serializer.data)

    def post(self,request):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can create a course"})
        serializer=CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=request.user.teacherprofile)
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can update a course"})
        course=Course.objects.get(id=pk,teacher__user=request.user)
        
        course.name=request.data.get('name')
        course.code=request.data.get('code')
        course.teacher=request.user.teacherprofile
        course.save()
        serializer=CourseSerializer(course)
        return Response(serializer.data)

    def delete(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can delete a course"})
        course=Course.objects.get(id=pk,teacher__user=request.user)
    
        course.delete()
        return Response({"message":"Course Deleted"})


class LessonAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, pk=None):
      if pk:
        if hasattr(request.user, 'teacherprofile'):
            lesson = Lesson.objects.get(
                id=pk,
                course__teacher__user=request.user
            )
        else:
            lesson = Lesson.objects.get(
                id=pk,
                course__enrollment__student__user=request.user
            )

        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

      if hasattr(request.user, 'teacherprofile'):
        lessons = Lesson.objects.filter(
            course__teacher__user=request.user
        )
      else:
        lessons = Lesson.objects.filter(
            course__enrollment__student__user=request.user
        )

      serializer = LessonSerializer(lessons, many=True)
      return Response(serializer.data)
    
    def post(self,request):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can create a lesson"})
        serializer=LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can update a lesson"})
        lesson=Lesson.objects.get(id=pk,course__teacher__user=request.user)
        lesson.title=request.data.get('title')
        lesson.video=request.data.get('video')
        lesson.notes=request.data.get('notes')
        lesson.save()
        serializer=LessonSerializer(lesson)
        return Response(serializer.data)

    def delete(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can delete a lesson"})
        lesson=Lesson.objects.get(id=pk,course__teacher__user=request.user)
        lesson.delete()
        return Response({"message":"Lesson Deleted"})


class AssignmentAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None):
        if pk:
            if hasattr(request.user,'teacherprofile'):
                assignment=Assignment.objects.get(id=pk,course__teacher__user=request.user)
            else:
                assignment=Assignment.objects.get(id=pk,course__enrollment__student__user=request.user)
        
            serializer=AssignmentSerializer(assignment)
            return Response(serializer.data)
        if hasattr(request.user,'teacherprofile'):
            assignment=Assignment.objects.filter(course__teacher__user=request.user)
        else:
            assignment=Assignment.objects.filter(course__enrollment__student__user=request.user)
        serializer=AssignmentSerializer(assignment,many=True)
        return Response(serializer.data)
    def post(self,request):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can create an assignment"})
        serializer=AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can update an assignment"})
        assignment=Assignment.objects.get(id=pk,course__teacher__user=request.user)
        assignment.title=request.data.get('title')
        assignment.description=request.data.get('description')
        assignment.duedate=request.data.get('duedate')
        assignment.save()
        serializer=AssignmentSerializer(assignment)
        return Response(serializer.data)

    def delete(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can delete an assignment"})
        assignment=Assignment.objects.get(id=pk,course__teacher__user=request.user)
        assignment.delete()
        return Response({"message":"Assignment deleted"})


class QuizAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None):
        if pk:
            if hasattr(request.user,'teacherprofile'):
                quiz=Quiz.objects.get(id=pk,course__teacher__user=request.user)
            else:
                quiz=Quiz.objects.get(id=pk,course__enrollment__student__user=request.user)
        
            serializer=QuizSerializer(quiz)
            return Response(serializer.data)
        if hasattr(request.user,'teacherprofile'):
            quiz=Quiz.objects.filter(course__teacher__user=request.user)
        else:
            quiz=Quiz.objects.filter(course__enrollment__student__user=request.user)
        serializer=QuizSerializer(quiz,many=True)
        return Response(serializer.data)

    def post(self,request):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can create a quiz"})
        serializer=QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can update a quiz"})
        quiz=Quiz.objects.get(id=pk,course__teacher__user=request.user)
        quiz.title=request.data.get('title')
        quiz.duedate=request.data.get('duedate')
        quiz.save()
        serializer=QuizSerializer(quiz)
        return Response(serializer.data)

    def delete(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can delete a quiz"})
        quiz=Quiz.objects.get(id=pk,course__teacher__user=request.user)
        quiz.delete()
        return Response({"message":"Quiz Deleted"})

class QuestionAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None):
        if pk:
            if hasattr(request.user,'teacherprofile'):
               question=Question.objects.get(id=pk,quiz__course__teacher__user=request.user)
            else:
                question=Question.objects.get(id=pk,quiz__course__enrollment__student__user=request.user)
            serializer=QuestionSerializer(question)
            return Response(serializer.data)
        if hasattr(request.user,'teacherprofile'):
            question=Question.objects.filter(quiz__course__teacher__user=request.user)
        else:
            question=Question.objects.filter(quiz__course__enrollment__student__user=request.user)
        serializer=QuestionSerializer(question,many=True)
        return Response(serializer.data)

    def post(self,request):
            if not hasattr(request.user,'teacherprofile'):
                return Response({"message":"Only teachers can create the question"})
            serializer=QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

    def put(self,request,pk):
            if not hasattr(request.user,'teacherprofile'):
                return Response({"message":"Only teachers can update the question"})
            question=Question.objects.get(id=pk,quiz__course__teacher__user=request.user)
            question.question=request.data.get('question')
            question.marks=request.data.get('marks')
            question.save()
            serializer=QuestionSerializer(question)
            return Response(serializer.data)

    def delete(self,request,pk):
            if not hasattr(request.user,'teacherprofile'):
                return Response({"message":"Only teachers can delete the question"})
            question=Question.objects.get(id=pk,quiz__course__teacher__user=request.user)
            question.delete()
            return Response({"message":"Question Deleted"})

class OptionAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None):
        if pk:
            if hasattr(request.user,'teacherprofile'):
               option=Option.objects.get(id=pk,question__quiz__course__teacher__user=request.user)
            else:
                option=Option.objects.get(id=pk,question__quiz__course__enrollment__student__user=request.user)
            serializer=OptionSerializer(option)
            return Response(serializer.data)
        if hasattr(request.user,'teacherprofile'):
            option=Option.objects.filter(question__quiz__course__teacher__user=request.user)
        else:
            option=Option.objects.filter(question__quiz__course__enrollment__student__user=request.user)
        serializer=OptionSerializer(option,many=True)
        return Response(serializer.data)
    def post(self,request):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can create the options"})
        serializer=OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can update the options"})
        option=Option.objects.get(id=pk,question__quiz__course__teacher__user=request.user)
        option.option_text=request.data.get('option_text')
        option.is_correct=request.data.get('is_correct')
        option.save()
        serializer=OptionSerializer(option)
        return Response(serializer.data)

    def delete(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can delete the options"})
        option=Option.objects.get(id=pk,question__quiz__course__teacher__user=request.user)
        option.delete()
        return Response({"message":"Option Deleted"})
    

class EnrollmentAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None):
        if pk:
            if hasattr(request.user,'teacherprofile'):
               enrollment=Enrollment.objects.get(id=pk,course__teacher__user=request.user)
            else:
                enrollment=Enrollment.objects.get(id=pk,student__user=request.user)
            serializer=EnrollmentSerializer(enrollment)
            return Response(serializer.data)
        if hasattr(request.user,'teacherprofile'):
            enrollment=Enrollment.objects.filter(course__teacher__user=request.user)
        else:
            enrollment=Enrollment.objects.filter(student__user=request.user)
        serializer=EnrollmentSerializer(enrollment,many=True)
        return Response(serializer.data)

    def post(self,request):
            if not hasattr(request.user,'studentprofile'):
                return Response({"message":"Only students can enter into it"})
            serializer=EnrollmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(student=request.user.studentprofile)
                return Response(serializer.data)
            return Response(serializer.errors)
    
    def put(self,request,pk):
        if not hasattr(request.user,'studentprofile'):
            return Response({"message":"Only students can update it"})
        enrollment=Enrollment.objects.get(id=pk,student__user=request.user)
        enrollment.enrolled_date=request.data.get('enrolled_date')
         
        enrollment.save()
        serializer=EnrollmentSerializer(enrollment)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        if not hasattr(request.user,'studentprofile'):
            return Response({"message":"Only students can delete it"})
        enrollment=Enrollment.objects.get(id=pk,student__user=request.user)
        enrollment.delete()
        return Response({"message":"Enrollment Deleted"})

class ResultAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk=None):
        if pk:
            if hasattr(request.user,'teacherprofile'):
               result=Result.objects.get(id=pk,quiz__course__teacher__user=request.user)
            else:
                result=Result.objects.get(id=pk,student__user=request.user)
            serializer=ResultSerializer(result)
            return Response(serializer.data)
        if hasattr(request.user,'teacherprofile'):
            result=Result.objects.filter(quiz__course__teacher__user=request.user)
        else:
            result=Result.objects.filter(student__user=request.user)
        serializer=ResultSerializer(result,many=True)
        return Response(serializer.data)

    def post(self,request):
            if not hasattr(request.user,'teacherprofile'):
                return Response({"message":"Only teachers can create the result"})
            serializer=ResultSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
    
    def put(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can update the result"})
        result=Result.objects.get(id=pk,quiz__course__teacher__user=request.user)
        result.score=request.data.get('score')
        result.attempted_date=request.data.get('attempted_date')
        result.save()
        serializer=ResultSerializer(result)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only teachers can delete the result"})
        result=Result.objects.get(id=pk,quiz__course__teacher__user=request.user)
        result.delete()
        return Response({"message":"Result Deleted"})

class ProgressAPI(APIView):
    permission_classes=[IsTeacher]
    def get(self,request,pk=None):
        if pk:
            hasattr(request.user,'teacherprofile')
            progress=Progress.objects.get(id=pk,course__teacher__user=request.user)
        
            serializer=ProgressSerializer(progress)
            return Response(serializer.data)
        hasattr(request.user,'teacherprofile')
        progress=Progress.objects.filter(course__teacher__user=request.user)
        
        serializer=ProgressSerializer(progress,many=True)
        return Response(serializer.data)

    def post(self,request):
            if not hasattr(request.user,'teacherprofile'):
                return Response({"message":"Only the teacher can create the progress"})
            serializer=ProgressSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
    
    def put(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only the teacher can update the progress"})
        progress=Progress.objects.get(id=pk,course__teacher__user=request.user)
        progress.progresspercenatge=request.data.get('progresspercenatge')
        progress.last_accessed=request.data.get('last_accessed')
        progress.completedlesson=request.data.get('completedlesson')
        progress.save()
        serializer=ProgressSerializer(progress)
        return Response(serializer.data)
    
    def delete(self,request,pk):
        if not hasattr(request.user,'teacherprofile'):
            return Response({"message":"Only the teacher can delete the progress"})
        progress=Progress.objects.get(id=pk,course__teacher__user=request.user)
        progress.delete()
        return Response({"message":"Progress Deleted"})

# clear chat -> getting chat history -> adding the question to the chat -> finding out the answer -> saving that particular session

def assistant(request):

    # Clear chat this is the name given for the html button -> clear_chat
    if request.method == "POST" and request.POST.get("clear_chat"):

        request.session["ai_messages"] = []
        request.session.modified = True

        return redirect("assistant")


    # Get chat history if there is no history it gives []
    messages = request.session.get("ai_messages", [])

   # POST means the user has submitted something through the form

    if request.method == "POST":
    # gets the question is there is no question then "" ans strip i sused to remove unneccessary whitespaces from the beginning and end.
        question = request.POST.get("question", "").strip()

        if question:

            # Add question
            messages.append({
                "role": "user",
                "content": question
            })


            # Send conversation to Ollama
            response = ollama.chat(
                model="gemma3:1b",

                messages=[
                    {
                        "role": "system",
                       "content": """
                            You are an AI learning assistant.

                            Explain concepts simply and clearly.
                            Keep answers short and beginner-friendly.
                            Use examples only when useful.
                            For simple questions, answer in 3-5 sentences.
                            For programming questions, explain the logic briefly.
                            Avoid unnecessary details.
                        """
                    }
                ] + messages
            )


            # Get AI answer
            answer = response["message"]["content"]


            # Add AI answer
            messages.append({
                "role": "assistant",
                "content": answer
            })


            # Save conversation
            request.session["ai_messages"] = messages
            request.session.modified = True


        return redirect("assistant")


    return render(
        request,
        "assistant.html",
        {
            "messages": messages
        }
    )

class CourseDetailStudent(DetailView):
    model=Course
    template_name='coursedet.html'
    context_object_name='course'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self.request.user,'studentprofile'):
            return redirect("TeacherDashBoard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['lessons']=Lesson.objects.filter(course=self.object)
        context['assignments']=Assignment.objects.filter(course=self.object)
        context['quizes']=Quiz.objects.filter(course=self.object)
        context['announcements']=Announcements.objects.filter(course=self.object)
        return context

    def get_queryset(self):
        return Course.objects.filter(enrollment__student__user=self.request.user)




       
   