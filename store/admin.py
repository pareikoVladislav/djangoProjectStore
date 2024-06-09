from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.models import Book, Publisher, Post, CustomUser
from django.utils.translation import gettext_lazy


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (gettext_lazy('Required Fields'), {"fields": ('username', 'password')}),
        (gettext_lazy('Personal Info'), {"fields": ('first_name', 'last_name', 'email', 'age', 'birth_date')}),
        (gettext_lazy('Permissions'), {"fields": ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (gettext_lazy('Important Dates'), {"fields": ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            "classes": ('wide', ),
            "fields": ('username', 'password1', 'password2')
        }),
    )

    list_display = ('username', 'email', 'age', 'birth_date')
    search_fields = ('email', 'username')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'published_date')
    search_fields = ('title', 'author')
    list_filter = ('author',)
    ordering = ('-author', 'title')
    # fields = ('title',)
    list_per_page = 2


# class BookInLine(admin.TabularInline):
#     model = Book
#     extra = 1

class BookInLine(admin.StackedInline):
    model = Book
    extra = 1


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    inlines = [BookInLine]
    list_display = ('name', 'register_date')
    # fields = ('name', 'register_date')
    readonly_fields = ('register_date',)


# admin.site.register(Publisher, PublisherAdmin)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
