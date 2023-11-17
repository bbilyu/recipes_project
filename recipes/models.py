from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from slugify import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url_all(self):
        return reverse('category_all', kwargs={'cat_slug': self.slug})

    def get_absolute_url_user(self):
        return reverse('category_user', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Recipe(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    steps = models.TextField(blank=True, verbose_name="Шаги приготовления")
    cooking_time = models.PositiveIntegerField(blank=True, verbose_name="Время приготовления")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ManyToManyField(Category, through='RecipeCategory', verbose_name="Категории")

    def save(self, *args, **kwargs):
        if not self.slug:  # Проверяем, если slug не был задан
            self.slug = slugify(self.title)  # Формируем slug из заголовка
        super(Recipe, self).save(*args, **kwargs)  # Сохраняем объект


    def get_absolute_url_show(self):
        return reverse('recipe', kwargs={'recipe_slug': self.slug})

    def get_absolute_url_edit(self):
        return reverse('edit_recipe', kwargs={'recipe_slug': self.slug})

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        ordering = ['id']

    def __str__(self):
        return self.title


class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT)
