from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Drink, Category, TagDrink, DrinkMeta, Comment


class HasTagsFilter(admin.SimpleListFilter):
    title = 'Наличие тегов'
    parameter_name = 'has_tags'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'С тегами'),
            ('no', 'Без тегов'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(tags__isnull=False).distinct()

        if self.value() == 'no':
            return queryset.filter(tags__isnull=True)

        return queryset


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'post_photo',
        'author',
        'type',
        'brand',
        'available',
        'category',
        'short_description',
        'tags_count',
        'likes_count',
        'dislikes_count',
        'reposts_count',
        'time_create',
    )

    list_display_links = ('name',)
    list_editable = ('available',)
    ordering = ('-time_create', 'name')
    list_per_page = 10

    search_fields = (
        'name',
        'description',
        'type',
        'brand',
        'category__name',
        'tags__name',
    )

    list_filter = (
        'available',
        'category',
        'tags',
        HasTagsFilter,
        'time_create',
    )

    actions = (
        'set_available',
        'set_unavailable',
    )

    fields = (
        'name',
        'slug',
        'type',
        'brand',
        'description',
        'photo',
        'post_photo',
        'available',
        'category',
        'tags',
        'meta',
        'author',
        'liked_by',
        'disliked_by',
        'reposted_by',
        'time_create',
        'time_update',
    )

    readonly_fields = (
        'post_photo',
        'time_create',
        'time_update',
    )

    prepopulated_fields = {
        'slug': ('name',),
    }

    filter_horizontal = (
        'tags',
        'liked_by',
        'disliked_by',
        'reposted_by',
    )

    @admin.display(description='Изображение')
    def post_photo(self, drink):
        if drink.photo:
            return format_html(
                '<img src="{}" width="70" height="70" '
                'style="object-fit: cover; border-radius: 6px;">',
                drink.photo.url
            )

        return 'Без изображения'


    @admin.display(description='Краткое описание')
    def short_description(self, drink):
        if not drink.description:
            return 'Описание отсутствует'

        if len(drink.description) > 60:
            return f'{drink.description[:60]}...'

        return drink.description

    @admin.display(description='Количество тегов')
    def tags_count(self, drink):
        return drink.tags.count()

    @admin.display(description='Лайки')
    def likes_count(self, drink):
        return drink.liked_by.count()

    @admin.display(description='Дизлайки')
    def dislikes_count(self, drink):
        return drink.disliked_by.count()

    @admin.display(description='Репосты')
    def reposts_count(self, drink):
        return drink.reposted_by.count()

    @admin.action(
        description='Сделать выбранные напитки доступными'
    )
    def set_available(self, request, queryset):
        count = queryset.update(
            available=Drink.Availability.AVAILABLE
        )

        self.message_user(
            request,
            f'Доступными отмечено напитков: {count}.',
            messages.SUCCESS,
        )

    @admin.action(
        description='Сделать выбранные напитки недоступными'
    )
    def set_unavailable(self, request, queryset):
        count = queryset.update(
            available=Drink.Availability.NOT_AVAILABLE
        )

        self.message_user(
            request,
            f'Недоступными отмечено напитков: {count}.',
            messages.WARNING,
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(TagDrink)
class TagDrinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(DrinkMeta)
class DrinkMetaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'volume_ml',
        'package',
        'country',
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'drink',
        'author',
        'short_text',
        'time_create',
    )

    list_display_links = (
        'id',
        'short_text',
    )

    search_fields = (
        'text',
        'drink__name',
        'author__username',
    )

    list_filter = (
        'time_create',
    )

    ordering = (
        '-time_create',
    )

    @admin.display(description='Комментарий')
    def short_text(self, comment):
        if len(comment.text) > 60:
            return f'{comment.text[:60]}...'

        return comment.text