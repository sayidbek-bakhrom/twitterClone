from django.contrib import admin
from django.contrib.auth.models import Group, User


# unregister groups
admin.site.unregister(Group)


class UserAdmin