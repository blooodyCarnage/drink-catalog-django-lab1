from django.contrib import admin, messages

from .models import Drink, Category, TagDrink, DrinkMeta


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
        'type',
        'brand',
        'available',
        'category',
        'short_description',
        'tags_count',
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
        'available',
        'category',
        'tags',
        'meta',
        'time_create',
        'time_update',
    )

    readonly_fields = (
        'time_create',
        'time_update',
    )

    prepopulated_fields = {
        'slug': ('name',),
    }

    filter_horizontal = ('tags',)

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