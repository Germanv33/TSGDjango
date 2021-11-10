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








class WaterKeep(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Жилец', blank = True)
    pair_count = models.IntegerField(verbose_name='Количество пар счетчиков', blank="Количество пар счетчиков", default=1)
    hot1 = models.IntegerField(verbose_name='Номер 1 горячего счетчика', blank="Номер 1 горячего счетчика", null = True)
    cold1 = models.IntegerField(verbose_name='Номер 1 холодного счетчика', blank="Номер 1 холодного счетчика", null = True)
    hot2 = models.IntegerField(verbose_name='Номер 2 горячего счетчика', blank="Номер 1 горячего счетчика", null = True )
    cold2 = models.IntegerField(verbose_name='Номер 2 холодного счетчика', blank="Номер 1 холодного счетчика", null = True )
    hot3 = models.IntegerField(verbose_name='Номер 3 горячего счетчика', blank="Номер 1 горячего счетчика", null = True )
    cold3 = models.IntegerField(verbose_name='Номер 3 холодного счетчика', blank="Номер 1 холодного счетчика", null = True )
    hot4 = models.IntegerField(verbose_name='Номер 4 горячего счетчика', blank="Номер 1 горячего счетчика", null = True )
    cold4 = models.IntegerField(verbose_name='Номер 4 холодного счетчика', blank="Номер 1 холодного счетчика", null = True )
    hot5 = models.IntegerField(verbose_name='Номер 5 горячего счетчика', blank="Номер 1 горячего счетчика", null = True )
    cold5 = models.IntegerField(verbose_name='Номер 5 холодного счетчика', blank="Номер 1 холодного счетчика", null = True )
    hot6 = models.IntegerField(verbose_name='Номер 6 горячего счетчика', blank="Номер 1 горячего счетчика", null = True )
    cold6 = models.IntegerField(verbose_name='Номер 6 холодного счетчика', blank="Номер 1 холодного счетчика", null = True )

    class Meta:
        verbose_name='Номера счетчиков'
        verbose_name_plural='Номера счетчиков'

    def __str__(self) -> str:
        return f"Счетчики {self.user.kvartira} квартиры"

class Water(models.Model):

    kvartira = models.IntegerField(verbose_name='Квартира', blank="Квартира")
    create_date = models.DateTimeField(auto_now=True)

    hot1 = models.IntegerField(verbose_name='1 горячего счетчика', blank="1 горячего счетчика")
    cold1 = models.IntegerField(verbose_name='1 холодного счетчика', blank="1 холодного счетчика" )
    hot2 = models.IntegerField(verbose_name='2 горячего счетчика', blank="1 горячего счетчика", null = True )
    cold2 = models.IntegerField(verbose_name='2 холодного счетчика', blank="1 холодного счетчика", null = True )
    hot3 = models.IntegerField(verbose_name= '3 горячего счетчика', blank="1 горячего счетчика", null = True )
    cold3 = models.IntegerField(verbose_name= '3 холодного счетчика', blank="1 холодного счетчика", null = True )
    hot4 = models.IntegerField(verbose_name='4 горячего счетчика', blank="1 горячего счетчика", null = True )
    cold4 = models.IntegerField(verbose_name='4 холодного счетчика', blank="1 холодного счетчика", null = True )
    hot5 = models.IntegerField(verbose_name='5 горячего счетчика', blank="1 горячего счетчика", null = True )
    cold5 = models.IntegerField(verbose_name='5 холодного счетчика', blank="1 холодного счетчика", null = True )
    hot6 = models.IntegerField(verbose_name='6 горячего счетчика', blank="1 горячего счетчика", null = True )
    cold6 = models.IntegerField(verbose_name='6 холодного счетчика', blank="1 холодного счетчика", null = True )

    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Дата показания счетчиков', blank="Дата показания счетчиков")
    
    class Meta:
        verbose_name='Показания Счетчиков'
        verbose_name_plural='Показания Счетчиков'

    def __str__(self) -> str:
        return f"{self.kvartira} за {self.date}"

class Letter(models.Model):
    kvartira = models.IntegerField(verbose_name='Квартира', blank="Квартира")
    email = models.EmailField(verbose_name='Почта', blank="Email")
    text = models.TextField(verbose_name='Письмо')
    create_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Письмо от жителя'
        verbose_name_plural='Письма от жителей'


