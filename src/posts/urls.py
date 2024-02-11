from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostsHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('add_post/', views.AddPost.as_view(), name='add_post'),
    path('edit_post/<slug:post_slug>/', views.UpdatePost.as_view(), name='edit_post'),
    path('delete_post/<slug:post_slug>/', views.DeletePost.as_view(), name='delete_post'),
    path('contact/', views.AddFeedback.as_view(), name='contact'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('category/<slug:category_slug>/', views.PostsByCategory.as_view(), name='category'),

]
