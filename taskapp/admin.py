from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'is_completed')
    list_filter = ('is_completed', 'due_date', 'user')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Task, TaskAdmin)
