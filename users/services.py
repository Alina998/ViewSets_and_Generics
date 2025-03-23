from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission


def create_moderator_group(sender, **kwargs):
    group, created = Group.objects.get_or_create(name="Moderators")
    permissions = [
        "lms.view_course",
        "lms.view_lesson",
        "lms.change_course",
        "lms.change_lesson",
    ]
    for perm in permissions:
        permission = Permission.objects.get(codename=perm)
        group.permissions.add(permission)


post_migrate.connect(create_moderator_group)
