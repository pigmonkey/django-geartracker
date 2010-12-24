from django.contrib import admin
from geartracker.models import *

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("make", "model")}
    list_display = ('__unicode__', 'type', 'metric_weight', 'acquired')
    list_filter = ('archived', 'category', 'type', 'make', 'tags')
    search_fields = ('make', 'model')
    filter_horizontal = ('related', 'tags')
admin.site.register(Item, ItemAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('__unicode__', 'number_items')
admin.site.register(Category, CategoryAdmin)

class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('category', 'name', 'number_items')
    list_filter = ('category',)
admin.site.register(Type, TypeAdmin)

class ListItemRelationshipInline(admin.TabularInline):
    model = ListItem
    extra = 1

class ListAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = (ListItemRelationshipInline,)
    list_display = ('name', 'total_metric_weight', 'start_date', 'end_date',
        'public')
    list_filter = ('public',)
admin.site.register(List, ListAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'number_items')
admin.site.register(Tag, TagAdmin)
