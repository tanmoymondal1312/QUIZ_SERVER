from django.contrib import admin
from .models import AppUpdate, Quiz, QuizCategory


@admin.register(QuizCategory)
class QuizCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active', 'created_at')  # add slug
    list_display_links = ('id', 'name')  # make these clickable
    search_fields = ('name', 'slug')
    list_filter = ('is_active',)
    ordering = ('id',)



@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question',
        'category',
        'correct_ans',
        'like',
        'dislike',
        'created_at',
    )

    list_filter = ('category', 'correct_ans', 'created_at')
    search_fields = ('question',)
    ordering = ('id',)

    fieldsets = (
        ('Question Info', {
            'fields': ('category', 'question')
        }),
        ('Options', {
            'fields': ('optA', 'optB', 'optC', 'optD', 'correct_ans')
        }),
        ('Engagement', {
            'fields': ('like', 'dislike', 'seen_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('seen_by',)



@admin.register(AppUpdate)
class AppUpdateAdmin(admin.ModelAdmin):
    list_display = ("link", "is_update", "created_at")
    list_filter = ("is_update",)
    search_fields = ("link",)