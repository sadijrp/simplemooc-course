from django.db import models
from django.conf import settings

from taggit.managers import TaggableManager


class Thread(models.Model):
    title = models.CharField('Título', max_length=100)
    body = models.TextField('Mensagem')
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)
    tags = TaggableManager()

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        on_delete=models.CASCADE,
        related_name='threads')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-updated_at']


class Reply(models.Model):
    reply = models.TextField('Resposta')
    correct = models.BooleanField('Correta?', blank=True, default=False)

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        on_delete=models.CASCADE,
        related_name='replies')

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created_at']
