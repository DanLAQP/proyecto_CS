from django.contrib import admin
from .models import AppSingleton


@admin.register(AppSingleton)
class AppSingletonAdmin(admin.ModelAdmin):
	readonly_fields = ('pk', 'updated')
	list_display = ('site_name', 'login_count', 'updated')
	fields = ('site_name', 'login_count', 'updated')
