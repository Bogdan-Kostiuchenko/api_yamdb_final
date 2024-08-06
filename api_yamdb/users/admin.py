from django.contrib import admin

from users.models import YamdbUser


@admin.register(YamdbUser)
class YamdbUserAdmin(admin.ModelAdmin):
    list_display = ('confirmation_code',
                    'username',
                    'email',
                    'role',
                    'bio',
                    'pk')
    list_editable = ('role',)
    search_fields = ('username', 'role',)
