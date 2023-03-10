from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet

# unregister groups
admin.site.unregister(Group)

admin.site.register(Tweet)


# mix profile info into user info
class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]


# unregister initial user
admin.site.unregister(User)
# register user and profile
admin.site.register(User, UserAdmin)
