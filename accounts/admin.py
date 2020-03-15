from django.contrib import admin
from accounts.models import UserInformation, UserImage


class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sex', 'age')


admin.site.register(UserInformation, UserInformationAdmin)


class UserImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'image')


admin.site.register(UserImage, UserImageAdmin)
