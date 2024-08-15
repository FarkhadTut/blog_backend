from django.contrib import admin
from .models import *

from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils.html import format_html

@admin.register(User)
class PostAdmin(admin.ModelAdmin):  
    pass


# app_auth/admin.py




@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    # Ceates an easy way to view/expire current sessions
    list_display = ('session_key', 'username', 'expire_date',)

    def username(self, obj):
        session_data = obj.get_decoded()
        user_id = session_data.get('_auth_user_id')

        if user_id:
            user = User.objects.get(id=user_id)
            return user.username
        return None

    # def expire_session(self, obj):
    #     return format_html(
    #         '<a href="{}" class="button">Expire Session</a>',
    #         reverse('expire_session', args=[obj.pk])
    #     )