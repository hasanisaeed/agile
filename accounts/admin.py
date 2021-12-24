from django.contrib import admin

from accounts.models import CustomUser, Attendance, Sprint, StoryPoint


class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Attendance, CustomUserAdmin)
admin.site.register(Sprint, CustomUserAdmin)
admin.site.register(StoryPoint, CustomUserAdmin)
