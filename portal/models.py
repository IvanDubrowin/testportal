from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


class UserCurrentCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    stat_true_ans = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    del_ans = models.IntegerField(default=0)

    ans = {}

    def get_question(self):
        query = Question.objects.filter(course = self.course)
        questions = list(query)[self.del_ans:(self.count + 1)]
        return questions

    def true_answer(self):
        question = list(
            Question.objects.filter(course=self.course).values('true_ans')
        )
        try:
            self.ans.update(question[self.count])
        except IndexError:
            pass
        return self.ans

    def save_answer(self, form):
        self.count += 1
        self.del_ans += 1
        self.save()
        user_answer = int(form.data['field'])
        true_ans = int(self.ans['true_ans'])

        if user_answer == true_ans:
            self.stat_true_ans += 1
            self.save()

    def end_learn(self):
        self.ans.clear()
        self.count = 0
        self.del_ans = 0
        stat = UserCourseStat(
                        id_user=self.user,
                        id_course=self.course,
                        correct_answers=self.stat_true_ans,
                        total_answers=len(Question.objects.filter(course=self.course))
                    )
        stat.save()
        self.stat_true_ans = 0
        self.save()


class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    text_question = models.TextField()
    ans1 = models.TextField()
    ans2 = models.TextField()
    ans3 = models.TextField()
    ans4 = models.TextField()
    true_ans = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='Course')

    def __str__(self):
        return self.text_question


class UserCourseStat(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    total_answers = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Пользователь: %s, %s'  % (self.id_user, self.id_course)
