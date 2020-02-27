from django.contrib import admin
from accounts.models import UserInformation


class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'age')


admin.site.register(UserInformation, UserInformationAdmin)
