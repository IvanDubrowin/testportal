from django.db import models
from django.contrib.auth.models import User



class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name


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
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Пользователь: %s, %s'  % (self.id_user, self.id_course)
