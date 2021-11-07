from django.db import models
from django.contrib.auth.models import AbstractUser, User
from .middleware import get_current_user
from django.db.models import Q

# Create your models here.


class User(AbstractUser):
    kvartira = models.IntegerField(verbose_name='Квартира', blank="Квартира")

    class Meta:
        db_table='auth_user'
        abstract = True
        



class Articles(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Владелец статьи', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Статью'
        verbose_name_plural='Статьи'

class Documents(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Владелец статьи', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name='Название')
    file = models.CharField(max_length=250, verbose_name='Ссылка на файл')
    text = models.TextField(verbose_name='Текст')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Документы'
        verbose_name_plural='Документы'



class StatusFilterComments(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status=False, author = get_current_user()) | Q(status=False, article__author=get_current_user()) | Q(status=True))
    


class Comments(models.Model):
    article = models.ForeignKey(Articles, on_delete = models.CASCADE, verbose_name='Статья', blank = True, null = True,related_name='comments_articles' )
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)
    objects  = StatusFilterComments()


class User(AbstractUser):
    kvartira = models.IntegerField(verbose_name='Квартира', blank="Квартира", null=True)

    class Meta:
        db_table='auth_user'
