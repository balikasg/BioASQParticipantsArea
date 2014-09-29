from django.contrib import admin
from uploads.models import Document


class Admin_Doc(admin.ModelAdmin):
	list_display=('user', 'test_set')
admin.site.register(Document, Admin_Doc)
