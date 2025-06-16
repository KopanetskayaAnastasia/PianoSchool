import io
import openpyxl
from django.http import HttpResponse
from django.views import View
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Lesson, Subject, EducationPlan, Group
from users.models import Students, TestResult, TeacherStudent
from django.db.models import Q



class ProgressReportExportForm(forms.Form):
    section = forms.ChoiceField(label="Секция", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    student = forms.ModelChoiceField(queryset=Students.objects.none(), label="Ученик", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(queryset=Group.objects.none(), label="Группа", required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.ModelChoiceField(queryset=None, label="Предмет", required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['student'].queryset = Students.objects.filter(school=school)
            self.fields['subject'].queryset = Subject.objects.distinct()
        else:
            self.fields['subject'].queryset = Lesson.objects.none()
        if teacher:
            self.fields['group'].queryset = Group.objects.filter(teacher=teacher)
        else:
            self.fields['group'].queryset = Group.objects.none()
        # Секции формируются по всем урокам школы
        if school:
            sections = ['1 четверть', '2 четверть', '3 четверть', '4 четверть']
            self.fields['section'].choices = [('', 'Все секции')] + [(s, s) for s in sorted(sections)]
        else:
            self.fields['section'].choices = [('', 'Все секции')]



from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class GroupMembershipForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=Students.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Ученики"
    )

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher')
        students_queryset = kwargs.pop('students_queryset', None)  # <-- обработать до super()
        super().__init__(*args, **kwargs)
        if students_queryset is not None:
            self.fields['students'].queryset = students_queryset
        else:
            student_ids = TeacherStudent.objects.filter(teacher=teacher).values_list('student_id', flat=True)
            self.fields['students'].queryset = Students.objects.filter(pk__in=student_ids)