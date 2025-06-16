from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.forms import ModelForm, TextInput, PasswordInput, CharField
from django import forms
from .models import Students
from .models import Teachers

class StudentsForm(forms.ModelForm):
    GRADE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
    ]
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        input_formats=['%d.%m.%Y'],  # Указываем формат даты
        label='Дата рождения. Формат: ДД.ММ.ГГГГ'
    )
    grade_of_school = forms.ChoiceField(
        choices=GRADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Год обучения'
    )
    class Meta:
        model = Students
        fields = ['name', 'patronymic', 'surname', 'phone', 'school', 'grade_of_school', 'birth_date', 'instrument']
        labels = {
            'name': 'Имя',
            'patronymic': 'Отчество',
            'surname': 'Фамилия',
            'phone': 'Телефон',
            'school': 'Школа',
            'grade_of_school': 'Год обучения',
            'instrument': 'Инструмент',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7XXXXXXXXXX'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'instrument': forms.Select(attrs={'class': 'form-control'}),
        }


class TeachersForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        input_formats=['%d.%m.%Y'],  # Указываем формат даты
        label='Дата рождения. Формат: ДД.ММ.ГГГГ'
    )
    class Meta:
        model = Teachers
        fields = ['name','surname', 'patronymic', 'phone', 'school', 'subject', 'birth_date']
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'patronymic': 'Отчество',
            'phone': 'Телефон',
            'school': 'Школа',
            'subject': 'Предмет',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7XXXXXXXXXX'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }


class RegisterUserForm(UserCreationForm):
    ROLE_CHOICES = [
        ('teacher', 'Учитель'),
        ('student', 'Ученик'),
    ]
    username = CharField(label='Логин', widget=TextInput(attrs={'class': 'form-control'}))
    password1 = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}))
    password2 = CharField(label='Подтверждение пароля', widget=PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Роль', widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2', )
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']

        if commit:
            user.save()
            if role == 'teacher':
                group = Group.objects.get(name='Учителя')
            else:
                group = Group.objects.get(name='Ученики')
            user.groups.add(group)

        return user


class LoginUserForm(AuthenticationForm):
    username = CharField(label='Логин', widget=TextInput(attrs={'class': 'form-control'}))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={'class': 'form-control'}))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Логин',
            'email': 'Email',
        }
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
        }
