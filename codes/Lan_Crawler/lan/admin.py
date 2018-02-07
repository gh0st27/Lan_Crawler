from lan.models import Metadata
from django.contrib import admin
# from .models import Metadata
#
# admin.site.unregister(Metadata)
admin.site.register(Metadata)

# from lan.models import Metadata
# from django.contrib import admin
#
#
# class MetadataAdmin(admin.ModelAdmin):
#     list_display = ('Name', 'Path', 'Extension', 'Size', 'Date')
#     search_fields = ['Name']
#     date_hierarchy = 'Date'
#     admin.site.register(Metadata)
#     admin.site.register(Metadata)
