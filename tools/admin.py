__author__ = 'edilio'

from django.contrib import admin
from models import *

#class Parameter(models.Model):
#    tool = models.ForeignKey(Tool)
#    name = models.CharField(max_length=20)
#    description = models.TextField()

class ParameterInline(admin.TabularInline):
    model = Parameter

class ToolAdmin(admin.ModelAdmin):
    list_display = ('function_name','category','pub_date','author')
    list_filter = ('category','author')
    list_per_page = 15
    search_fields = ('code','description','function_name',)
    date_hierarchy = 'pub_date'
    inlines = [
        ParameterInline,
    ]
    def save_model(self, request, obj, form, change):
        user = request.user
        if getattr(obj, 'obj.author_id', None) is None:
            setattr(obj,'author', user)
        obj.save()

class CategoryAdmin(admin.ModelAdmin):
    pass


def register(model,admin_class):
    admin.site.register(model, admin_class)

register(Tool, ToolAdmin)
register(Category, CategoryAdmin)
