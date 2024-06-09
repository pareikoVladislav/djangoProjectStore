from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy
from django.utils import timezone
# from django.contrib.auth.models import User


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(gettext_lazy('Email address'), unique=True)
    first_name = models.CharField(
        gettext_lazy('First Name'),
        max_length=25,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        gettext_lazy('Last Name'),
        max_length=25,
        null=True,
        blank=True
    )
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'birth_date']


class Post(models.Model):
    title = models.CharField(max_length=170)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Publisher(models.Model):
    name = models.CharField(max_length=75)
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=75)
    published_date = models.DateField()
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        db_table = 'book'
        verbose_name = 'fiction book'
        verbose_name_plural = 'fiction books'
        ordering = ['published_date']
        unique_together = ('title', 'author')
        # index_together = ('title', 'author')
        indexes = [
            models.Index(fields=('title', 'author'), name='title_author_idx'),
            models.Index(fields=('published_date',), name='published_date_idx')
        ]
        get_latest_by = 'published_date'
