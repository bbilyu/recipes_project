from django.contrib import admin

from .models import Recipe, Category


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
