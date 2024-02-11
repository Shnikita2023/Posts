menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_post'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3
    title_page = None
    button_page = None
    button_delete = None
    category_selected = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context["title"] = self.title_page

        if self.button_page:
            self.extra_context["button"] = self.button_page

        if self.button_delete:
            self.extra_context["button_delete"] = self.button_delete

        if self.category_selected is not None:
            self.extra_context["category_selected"] = self.category_selected

    def get_mixin_context(self, context: dict, **kwargs: dict) -> dict:
        context['category_selected'] = None
        context.update(kwargs)
        return context
