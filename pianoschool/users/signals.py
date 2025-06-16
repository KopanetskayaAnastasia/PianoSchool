from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Students, Teachers

@receiver(m2m_changed, sender=User.groups.through)
def create_profile(sender, instance, action, **kwargs):
    if action == "post_add":
        # Проверяем, принадлежит ли пользователь к группе "Ученики"
        if instance.groups.filter(name='Ученики').exists():
            Students.objects.get_or_create(user=instance)
        # Проверяем, принадлежит ли пользователь к группе "Учителя"
        elif instance.groups.filter(name='Учителя').exists():
            Teachers.objects.get_or_create(user=instance)