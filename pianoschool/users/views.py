from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentsForm, TeachersForm, UserForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import RegisterUserForm, LoginUserForm
from .models import Students, Teachers, TeacherStudent



def personalisation(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "404.html", status=404)
    if user.groups.filter(name='Учителя').exists():
        profile_instance = Teachers.objects.filter(user=user).first()
        form_class = TeachersForm
    elif user.groups.filter(name='Ученики').exists():
        profile_instance = Students.objects.filter(user=user).first()
        form_class = StudentsForm
    else:
        return redirect('home')  # Перенаправление на главную, если пользователь не в группе

    if profile_instance is None:
        # Если профиль не найден, создайте новый экземпляр
        profile_instance = form_class.Meta.model(user=user)


    if request.method == 'POST':
        form = form_class(request.POST, instance=profile_instance)
        user_form = UserForm(request.POST, instance=user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            # Обновляем форму с сохраненными данными
            form = form_class(instance=profile_instance)
            user_form = UserForm(instance=user)
            return render(request, 'users/personalisation.html', {'form': form, 'user_form': user_form, 'saved': True})
    else:
        form = form_class(instance=profile_instance)
        user_form = UserForm(instance=user)

    return render(request, 'users/personalisation.html', {'form': form, 'user_form': user_form})



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.views import PasswordChangeDoneView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Пароль успешно изменён!")
        return redirect(reverse_lazy('personalisation'))

def delete_profile(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, "404.html", status=404)

    # Определяем профиль пользователя
    if user.groups.filter(name='Учителя').exists():
        profile = Teachers.objects.filter(user=user).first()
        if profile:
            # Удаляем все TeacherStudent, где этот учитель
            TeacherStudent.objects.filter(teacher=profile).delete()
    elif user.groups.filter(name='Ученики').exists():
        profile = Students.objects.filter(user=user).first()
        if profile:
            # Удаляем все TeacherStudent, где этот ученик
            TeacherStudent.objects.filter(student=profile).delete()
    else:
        return redirect('home')

    if request.method == 'POST':
        # Удаляем профиль, затем пользователя
        if profile:
            profile.delete()
        user.delete()
        logout(request)
        messages.success(request, "Ваш профиль был успешно удалён.")
        return redirect('home')
    else:
        # GET-запрос — подтверждение удаления
        return render(request, 'users/confirm_delete_profile.html', {'profile': profile})