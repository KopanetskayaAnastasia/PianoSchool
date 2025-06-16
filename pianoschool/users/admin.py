from django.contrib import admin
from .models import Students, Teachers, TeacherStudent, Instruments, TestResult


class TeachersInstanceInline(admin.TabularInline):
    model = TeacherStudent


class StudentsInstanceInline(admin.TabularInline):
    model = TeacherStudent

class StudentsModelAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'birth_date', 'phone', 'school', 'grade_of_school', 'created_at', 'updated', 'instrument')
    search_fields = ('surname', 'grade_of_school', 'instruments', 'school')
    inlines = [StudentsInstanceInline]

    class Meta:
        model = Students

admin.site.register(Students, StudentsModelAdmin)


class TeachersModelAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'phone', 'school', 'subject', 'birth_date', 'created_at', 'updated')
    search_fields = ('surname', 'subject', 'school')
    inlines = [TeachersInstanceInline]

    class Meta:
        model = Teachers

admin.site.register(Teachers, TeachersModelAdmin)


class TeacherStudentModelAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'student']

    class Meta:
        model = TeacherStudent

admin.site.register(TeacherStudent, TeacherStudentModelAdmin)

class InstrumentsModelAdmin(admin.ModelAdmin):
    list_display = ['name']

    class Meta:
        model = Instruments

admin.site.register(Instruments, InstrumentsModelAdmin)



class TestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'timestamp', 'score')
    list_filter = ('student', 'test')

admin.site.register(TestResult, TestResultAdmin)

