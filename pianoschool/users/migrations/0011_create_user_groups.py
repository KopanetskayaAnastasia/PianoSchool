from django.db import migrations


def create_user_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    # Создаём две группы, если их ещё нет
    Group.objects.get_or_create(name='Ученики')
    Group.objects.get_or_create(name='Учителя')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),  # <-- ссылается на твою миграцию выше
        ('auth', 'latest'),     # гарантирует, что таблицы групп уже созданы
    ]

    operations = [
        migrations.RunPython(create_user_groups, noop),
    ]