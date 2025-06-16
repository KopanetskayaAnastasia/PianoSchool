from contextlib import nullcontext

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator, EmailValidator,FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.utils.text import slugify


class School(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    building_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=6, validators=[RegexValidator(regex=r'^\d{6}$', message="Postal code must be 6 digits.")])
    phone = models.CharField(max_length=12, validators=[RegexValidator(regex=r'^\+7\d{10}$', message="Phone number must be entered in the format: '+7XXXXXXXXXX'.")])
    email = models.EmailField(validators=[EmailValidator(message="Enter a valid email address.")])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'

class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class EducationPlan(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    program_file =models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name} - {self.year} - {self.school.name}"

    class Meta:
        verbose_name = 'План обучения'
        verbose_name_plural = 'Планы обучения'


class Lesson(models.Model):
    slug = models.SlugField(null=True, unique=True, verbose_name="URL-идентификатор")
    content_file = models.JSONField(blank=True, null=True)
    topic = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    education_plan = models.ForeignKey(EducationPlan, on_delete=models.CASCADE)
    difficulty_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"Тема '{self.topic}' к разделу '{self.section}' по предмету '{self.education_plan.subject.name}'"

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.topic)
        super().save(*args, **kwargs)

    def get_next_lesson(self):
        """Возвращает следующий урок, если он существует"""
        if self.content_file and 'next_lesson_id' in self.content_file:
            next_id = self.content_file['next_lesson_id']
            if next_id:
                return Lesson.objects.filter(content_file__id=next_id, education_plan=self.education_plan).first()
        return None



class Test(models.Model):
    slug = models.SlugField(null=True, unique=True, verbose_name="URL-идентификатор")
    content = models.JSONField(blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.topic)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Тест для {self.lesson.topic}"

    def get_passing_score(self):
        """Возвращает проходной балл теста"""
        if self.content and 'test' in self.content and 'passing_score' in self.content['test']:
            return self.content['test']['passing_score']
        return 70  # Значение по умолчанию

    def get_total_points(self):
        """Возвращает максимальное количество баллов за тест"""
        if self.content and 'test' in self.content and 'questions' in self.content['test']:
            return sum(q.get('points', 0) for q in self.content['test']['questions'])
        return 0





class EarTrainingTest(models.Model):
    """Контрольная по слуховому анализу"""
    title = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='tests')
    section = models.CharField(max_length=50)  # Например, '1 четверть'
    description = models.TextField(blank=True)
    date_open = models.DateField()
    date_close = models.DateField()

    # Для удобства отображения в выпадающих списках
    def __str__(self):
        return f"{self.title} ({self.section})"

    class Meta:
        verbose_name = 'Контрольная слухового диктанта'
        verbose_name_plural = 'Контрольные слуховых диктантов'
        ordering = ['id']

class EarTrainingTask(models.Model):
    """Задание в контрольной"""
    TEST_TYPE_CHOICES = [
        ('recognition', 'Распознавание'),
        ('performance', 'Воспроизведение'),
    ]
    test = models.ForeignKey(EarTrainingTest, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES)
    question = models.CharField(max_length=255)
    reference_notes = models.JSONField()  # ['C', 'D', 'E', ...]
    options = models.JSONField(blank=True, null=True)  # Только для recognition
    correct_option = models.PositiveSmallIntegerField(blank=True, null=True)  # Только для recognition
    points = models.PositiveIntegerField(default=1, verbose_name="Баллы за задание")


    class Meta:
        verbose_name = 'Тест слухового диктанта'
        verbose_name_plural = 'Тесты слуховых диктантов'
        ordering = ['test__id', 'id']

class EarTrainingAttempt(models.Model):
    """Попытка ученика по заданию"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(EarTrainingTask, on_delete=models.CASCADE)
    attempt_number = models.PositiveSmallIntegerField(default=1)
    played_notes = models.JSONField(blank=True, null=True)  # Только для performance
    selected_option = models.PositiveSmallIntegerField(blank=True, null=True)  # Только для recognition
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Попытка ученика по заданию'
        verbose_name_plural = 'Попытки ученика по заданию'
        ordering = ['id']

class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название группы")
    teacher = models.ForeignKey('users.Teachers', on_delete=models.CASCADE, related_name="groups", verbose_name="Учитель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships", verbose_name="Группа")
    student = models.ForeignKey('users.Students', on_delete=models.CASCADE, related_name="group_memberships", verbose_name="Ученик")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата вступления")

    class Meta:
        unique_together = ('group', 'student')