from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, FormView, DeleteView)

from posts.forms import AddPostForm, AddFeedbackForm
from posts.models import Posts, TagPost
from posts.utils import DataMixin
from siteposts import settings


class PostsHome(DataMixin, ListView):
    template_name = "posts/index.html"
    context_object_name = "posts"
    title_page = "Главная страница"
    category_selected = 0

    def get_queryset(self):
        return Posts.published.select_related('category')


class ShowPost(DataMixin, DetailView):
    template_name = "posts/posts.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs: dict) -> dict:
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=context["post"].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Posts,
                                 slug=self.kwargs[self.slug_url_kwarg],
                                 is_published=Posts.Status.PUBLISHED)


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'posts/add_post.html'
    title_page = 'Добавление поста'
    button_page = "Добавить"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, DataMixin, UpdateView):
    model = Posts
    fields = ("title", "content", "photo", "is_published", "category", "tag")
    template_name = 'posts/add_post.html'
    success_url = reverse_lazy("home")
    slug_url_kwarg = "post_slug"
    title_page = 'Редактирование поста'
    button_page = "Изменить"

    def get_initial(self):
        initial = super().get_initial()
        initial['is_published'] = Posts.Status.PUBLISHED
        return initial

    def dispatch(self, request: HttpRequest, *args: tuple, **kwargs: dict):
        post = self.get_object()

        if post.author != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, user=self.request.user)


class DeletePost(DeleteView):
    model = Posts
    template_name = 'posts/delete_post.html'
    success_url = reverse_lazy("home")
    slug_url_kwarg = "post_slug"


class AddFeedback(LoginRequiredMixin, DataMixin, FormView):
    form_class = AddFeedbackForm
    template_name = 'posts/feedback.html'
    success_url = reverse_lazy("home")
    title_page = 'Обратная связь'
    button_page = "Отправить"

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        body = f'Имя: {name}\nEmail: {email}\nСообщение: {message}'

        try:
            send_mail(
                self.title_page,
                body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

        except BadHeaderError:
            raise

        return super().form_valid(form)


class PostsByCategory(DataMixin, ListView):
    template_name = "posts/index.html"
    context_object_name = "posts"
    allow_empty = True

    def get_queryset(self):
        category_slug = self.kwargs["category_slug"]
        return Posts.published.filter(category__slug=category_slug).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context["posts"][0].category
        return self.get_mixin_context(context=context,
                                      category_selected=category.pk,
                                      title="Категория - " + category.name)


class TagPostList(DataMixin, ListView):
    template_name = "posts/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        tag_slug = self.kwargs["tag_slug"]
        return Posts.objects.filter(tag__slug=tag_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.get_mixin_context(context=context,
                                      title="Тег - " + tag.tag)


def about(request):
    return render(request, 'posts/about.html')
