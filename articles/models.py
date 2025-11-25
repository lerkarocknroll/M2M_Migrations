from django.db import models


class Tag(models.Model):

    name = models.CharField(max_length=50, verbose_name='Раздел')

    class Meta:
        verbose_name = 'Раздел'

    def __str__(self):
        return self.name


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    tags = models.ManyToManyField(Tag, through='Scope', verbose_name='Раздел')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):
    is_main = models.BooleanField(default=False, verbose_name='Основной')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')  # ← ИЛИ лучше 'article_scopes'

    class Meta:
        verbose_name = 'Тематика статьи'
        # 👇 Добавьте это, чтобы нельзя было назначить >1 основного тега на статью:
        constraints = [
            models.UniqueConstraint(
                fields=['article'],
                condition=models.Q(is_main=True),
                name='one_main_scope_per_article'
            )
        ]

    def __str__(self):
        return f"{self.tag.name} ({'основной' if self.is_main else 'доп.'})"