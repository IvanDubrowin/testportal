from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Question, Course, UserCourseStat
from .forms import QuestionChoices


class RegisterFormView(FormView):
    
    form_class = UserCreationForm
    success_url = "accounts/login/"
    template_name = "registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class StatisticView(View, LoginRequiredMixin):

    template_name = 'stat.html'

    @method_decorator(login_required)
    def get(self, request):
        user = User.objects.get(username=request.user)
        stat = UserCourseStat.objects.filter(id_user=user)
        args = {"stat": stat }
        return render(request, self.template_name, args)


class CourseView(View, LoginRequiredMixin):

    template_name = 'course.html'
    stat_true_ans = 0
    count = 0
    del_ans = 0
    ans = {}

    @method_decorator(login_required)
    def get(self, request, pk):
        query = Question.objects.filter(course = pk)
        form = QuestionChoices()
        questions = list(query)[CourseView.del_ans:(CourseView.count + 1)]
        args = {"questions" : questions, "form" : form}

        return render(request, self.template_name, args)

    @method_decorator(login_required)
    def post(self, request, pk):
        question = list(
        Question.objects.filter(course=pk).values('true_ans')
        )
        try:
            CourseView.ans.update(question[CourseView.count])
        except IndexError:
            pass
        form = QuestionChoices(self.request.POST)

        if form.is_valid():
            user = User.objects.get(username=request.user)
            course = Course.objects.get(id=pk)
            CourseView.count += 1
            CourseView.del_ans += 1
            user_answer = int(form.data['field'])
            true_ans = int(CourseView.ans['true_ans'])

            if user_answer == true_ans:
                CourseView.stat_true_ans += 1

            if CourseView.count == len(question):
                CourseView.ans.clear()
                CourseView.count = 0
                CourseView.del_ans = 0
                stat = UserCourseStat(
                                    id_user=user,
                                    id_course=course,
                                    correct_answers=CourseView.stat_true_ans,
                                    total_answers=len(question))
                stat.save()
                CourseView.stat_true_ans = 0
                return redirect('portal:statistic')

        return redirect('portal:course', pk)
