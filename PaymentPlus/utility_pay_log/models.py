from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CreateModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Tag(models.Model):
    """Модель Тэгов."""
    name = models.CharField(verbose_name='Название', max_length=20)
    # color = ColorField(verbose_name='Хекс-код')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Category(CreateModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, '
                   'цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class PaymentRecord(CreateModel):
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в '
                   'будущем — можно делать отложенные публикации.')
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='records',
        verbose_name='Автор публикации'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='records',
        null=True,
        verbose_name='Категория'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='records',
        verbose_name='Теги',
        blank=False
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.pub_date



class PaymentCategoryAmount(models.Model):
    pass
