from django.contrib import admin
from django import forms

from .models import School, Subject, EducationPlan, Lesson, Test
import json

class SchoolModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'street', 'building_number', 'postal_code', 'phone', 'email')
    search_fields = ('name', 'city')

class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(School, SchoolModelAdmin)
admin.site.register(Subject, SubjectModelAdmin)


class EducationPlanAdmin(admin.ModelAdmin):
    list_display = ('subject', 'year', 'school', 'program_file')
    list_filter = ('year', 'school')
    search_fields = ('subject', 'school')
    ordering = ('year',)

admin.site.register(EducationPlan, EducationPlanAdmin)




class JSONEditorForm(forms.ModelForm):
    """Форма с текстовым полем для редактирования JSON"""
    json_editor = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
                                  required=False, label="JSON данные")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            json_field_name = self.get_json_field_name()
            json_data = getattr(self.instance, json_field_name)
            if json_data:
                self.fields['json_editor'].initial = json.dumps(json_data, indent=4, ensure_ascii=False)

    def clean_json_editor(self):
        json_text = self.cleaned_data.get('json_editor')
        if not json_text:
            return {}
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Неверный формат JSON: {str(e)}")

    def save(self, commit=True):
        json_field_name = self.get_json_field_name()
        json_data = self.cleaned_data.get('json_editor')
        setattr(self.instance, json_field_name, json_data)
        return super().save(commit)

    def get_json_field_name(self):
        """Переопределите этот метод в подклассах"""
        return 'json_data'

    class Meta:
        # Добавьте это, чтобы скрыть оригинальное поле
        exclude = []  # Будет заполнено в подклассах


class LessonAdminForm(JSONEditorForm):
    class Meta:
        model = Lesson
        exclude = ['content_file']  # Скрываем оригинальное поле

    def get_json_field_name(self):
        return 'content_file'


class TestAdminForm(JSONEditorForm):
    class Meta:
        model = Test
        exclude = ['content']  # Скрываем оригинальное поле

    def get_json_field_name(self):
        return 'content'


class TestAdmin(admin.ModelAdmin):
    form = TestAdminForm
    list_display = ('lesson', 'slug')
    prepopulated_fields = {'slug': ('topic',)}
    list_filter = ('lesson',)
    def get_questions_count(self, obj):
        if obj.content and 'test' in obj.content and 'questions' in obj.content['test']:
            return len(obj.content['test']['questions'])
        return 0

    def get_passing_score(self, obj):
        if obj.content and 'test' in obj.content and 'passing_score' in obj.content['test']:
            return f"{obj.content['test']['passing_score']}%"
        return '-'

    get_passing_score.short_description = 'Проходной балл'
    get_questions_count.short_description = 'Количество вопросов'

admin.site.register(Test, TestAdmin)


class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ('topic', 'section','education_plan', 'difficulty_level', 'slug')
    prepopulated_fields = {'slug': ('topic',)}
    list_filter = ('education_plan', 'difficulty_level')
    search_fields = ('topic', 'section', 'difficulty_level',)

admin.site.register(Lesson, LessonAdmin)



from .models import EarTrainingTest, EarTrainingTask, EarTrainingAttempt

class EarTrainingTaskInline(admin.TabularInline):
    model = EarTrainingTask
    extra = 0

class EarTrainingAttemptInline(admin.TabularInline):
    model = EarTrainingAttempt
    extra = 0


@admin.register(EarTrainingTest)
class EarTrainingTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'section', 'date_open', 'date_close')
    list_filter = ('section', 'lesson')
    search_fields = ('title',)
    inlines = [EarTrainingTaskInline]

@admin.register(EarTrainingTask)
class EarTrainingTaskAdmin(admin.ModelAdmin):
    list_display = ('question', 'test', 'task_type')
    list_filter = ('task_type', 'test')
    search_fields = ('question',)
    inlines = [EarTrainingAttemptInline]

@admin.register(EarTrainingAttempt)
class EarTrainingAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'attempt_number', 'is_correct', 'timestamp')
    list_filter = ('is_correct', 'task', 'user')
    search_fields = ('user__username', 'task__question')