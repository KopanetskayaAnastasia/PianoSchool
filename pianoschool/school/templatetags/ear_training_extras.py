from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def some_attempt_correct(attempts):
    """True, если среди попыток есть хотя бы одна правильная"""
    return any(a.is_correct for a in attempts)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def some_attempt_correct(attempts):
    """True, если среди попыток есть хотя бы одна правильная"""
    return any(a.is_correct for a in attempts)

@register.filter
def points_for_task(attempts, task):
    """Возвращает баллы за задание для ученика (если правильно — task.points, иначе 0)"""
    if attempts and any(a.is_correct for a in attempts):
        return task.points
    return 0

@register.filter
def points_for_student(tasks_and_attempts):
    total = 0
    count = 0
    for task, attempts in tasks_and_attempts:
        count += 1
        if attempts and any(a.is_correct for a in attempts):
            total += task.points
    if count == 0:
        return 0
    return round(total / count, 2)

@register.filter
def student_points(tasks_and_attempts):
    """Сумма баллов, набранных учеником"""
    return sum(task.points for task, attempts in tasks_and_attempts if attempts and any(a.is_correct for a in attempts))

@register.filter
def max_points(tasks_and_attempts):
    """Максимально возможная сумма баллов"""
    return sum(task.points for task, attempts in tasks_and_attempts)


@register.filter
def average(items, field):
    items = list(items)
    if not items:
        return 0
    total = sum(getattr(item, field, 0) if hasattr(item, field) else item.get(field, 0) for item in items)
    return round(total / len(items), 2)