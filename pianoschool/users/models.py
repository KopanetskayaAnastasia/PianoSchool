from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

from school.models import School, Lesson, Test

from school.models import Subject


class Instruments(models.Model):
    name = models.CharField(verbose_name='Название инструмента', max_length=100)

    def __str__(self):
        return self.name

    def get_pk(self):
        return self.pk

    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'


class Teachers(models.Model):
    name = models.CharField(verbose_name='Фио', max_length=100, null=True)
    patronymic = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255,null=True)
    phone = models.CharField(null=True, default='+70000000000', max_length=12, validators=[
        RegexValidator(regex=r'^\+7\d{10}$', message="Phone number must be entered in the format: '+7XXXXXXXXXX'.")])
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True)
    birth_date = models.DateField(null=True)
    created_at = models.DateTimeField(verbose_name='Дата регистрации', auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    def __str__(self):
        return f"{self.surname} {self.name}"

    def get_pk(self):
        return self.pk

    def get_absolute_url(self):
        return f'/users/{self.id}'

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Students(models.Model):
    name = models.CharField(null=True, verbose_name='Фио', max_length=100)
    patronymic = models.CharField(null=True, max_length=255, blank=True)
    surname = models.CharField(null=True, max_length=255)
    birth_date = models.DateField(null=True)
    phone = models.CharField(null=True, default='+70000000000',max_length=12, validators=[RegexValidator(regex=r'^\+7\d{10}$', message="Phone number must be entered in the format: '+7XXXXXXXXXX'.")])
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    grade_of_school = models.IntegerField(null=True, verbose_name='Год обучения')
    created_at = models.DateTimeField(verbose_name='Дата регистрации', auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    instrument = models.ForeignKey(Instruments, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f"{self.surname} {self.name}"

    def get_pk(self):
        return self.pk

    def get_absolute_url(self):
        return f'/users/{self.id}'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class TeacherStudent(models.Model):
    teacher = models.ForeignKey(Teachers, on_delete=models.PROTECT, null=True)
    student = models.ForeignKey(Students, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.teacher.__str__() + " " + self.student.__str__()

    def get_pk(self):
        return self.pk

    class Meta:
        verbose_name = 'Связь учитель-ученик'
        verbose_name_plural = 'Связи учителя-ученики'



class TestResult(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    correct_count = models.IntegerField(null=True)
    incorrect_count = models.IntegerField(null=True)
    max_score = models.IntegerField(null=True)
    attempt_number = models.IntegerField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)  # Можно хранить ответы

    class Meta:
        unique_together = ('student', 'test')
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'

    def __str__(self):
        return f"{self.student} - {self.test} (Попытка {self.attempt_number})"