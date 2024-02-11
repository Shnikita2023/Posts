from .utils import menu


def get_post_context(request):
    return {"mainmenu": menu}
