from django.db.models import Count

from recipes.models import Category


main_menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "Рецепты", 'url_name': 'all'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]
additional_menu = [{'title': "Все рецепты", 'url_name': 'all'},
        {'title': "Мои рецепты", 'url_name': 'user'},
        {'title': "Добавить рецепт", 'url_name': 'add_recipe'},
        ]

class DataMixin:
    paginate_by = 10
    def get_user_context(self, **kwargs):
        context = kwargs
        if context['title'] != 'Главная':
            if 'author_id' in context:
                _author_id  = context['author_id']
                cats = Category.objects.filter(recipe__author_id=_author_id).distinct().annotate(Count('recipe'))
            else:
                cats = Category.objects.annotate(Count('recipe'))
            context['cats'] = cats
        user_main_menu = main_menu.copy()
        user_additional_menu = additional_menu.copy()

        context['main_menu'] = user_main_menu
        context['additional_menu'] = user_additional_menu
        
        if  context['title'] == "Все рецепты":
            context['cat_selected'] = 0
        return context
