from django.contrib import admin
from .models import AccentData

# Register your models here.

class AccentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'predicted_accent', 'is_correct_prediction')
    list_display_links = ('file_name', 'predicted_accent')

admin.site.register(AccentData, AccentAdmin)