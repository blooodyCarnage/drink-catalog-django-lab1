from .models import Category, TagDrink


class DataMixin:
    paginate_by = 3

    def get_mixin_context(self, context, **kwargs):
        context['categories'] = Category.objects.all()
        context['tags'] = TagDrink.objects.all()

        context.setdefault(
            'selected_category',
            None
        )
        context.setdefault(
            'selected_tag',
            None
        )

        if (
            hasattr(self, 'object_list')
            and self.object_list is not None
        ):
            context['drink_names'] = list(
                self.object_list.values_list(
                    'name',
                    flat=True
                )
            )

        context.update(kwargs)

        return context