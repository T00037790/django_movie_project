from django.contrib import admin
from .models import MoviePerson, Movie, MovieRate


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie, AuthorAdmin)
admin.site.register(MoviePerson, AuthorAdmin)
admin.site.register(MovieRate, AuthorAdmin)
