from django.contrib import admin
from .models import UserData

@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'mobile_number',
        'level',
        'mcq_completed',
        'mcq_solved',
        'is_paid',
    )
    list_select_related = ('user',)
    search_fields = ('user__username', 'user__email', 'mobile_number')
    list_filter = ('is_paid', 'level')
