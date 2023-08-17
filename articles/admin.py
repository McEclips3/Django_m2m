from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Article, ArticleTags, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ArticleTag(BaseInlineFormSet):
    def clean(self):
        if len(self.forms) == 0:
            raise ValidationError('Вы не указали теги=(')

        count_main = 0

        for f in self.forms:
            if count_main > 0 and f.cleaned_data.get('is_main'):
                raise ValidationError('Only one main tag')
            else:
                if f.cleaned_data.get('is_main'):
                    print(f'{f.cleaned_data.get("tag")} - главный раздел')
                    count_main += 1
                else:
                    continue

        return super().clean()


class ArticleTagsInline(admin.TabularInline):
    model = ArticleTags
    formset = ArticleTag
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    inlines = [ArticleTagsInline]


