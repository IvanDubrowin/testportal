from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Question, Course, UserCourseStat, UserCurrentCourse
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
        stat = UserCourseStat.objects.filter(id_user=user).order_by('-date')
        args = {"stat": stat }
        return render(request, self.template_name, args)


class CourseView(View, LoginRequiredMixin):

    template_name = 'course.html'

    @method_decorator(login_required)
    def get(self, request, pk):
        try:
            user_learning = UserCurrentCourse.objects.get(user=request.user, course=pk)
        except UserCurrentCourse.DoesNotExist:
            user_learning = UserCurrentCourse(
                        user = request.user,
                        course = Course.objects.get(id=pk)
                    )
            user_learning.save()

        form = QuestionChoices()
        args = {"questions" : user_learning.get_question(), "form" : form}
        return render(request, self.template_name, args)

    @method_decorator(login_required)
    def post(self, request, pk):
        user_learning = UserCurrentCourse.objects.get(user=request.user, course=pk)
        user_learning.true_answer()
        form = QuestionChoices(self.request.POST)

        if form.is_valid():
            user_learning.save_answer(form)
            if user_learning.count == len(Question.objects.filter(course=user_learning.course)):
                user_learning.end_learn()
                return redirect('portal:statistic')

        return redirect('portal:course', pk)
