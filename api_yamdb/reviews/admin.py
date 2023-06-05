from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
