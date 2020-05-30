from blog.api.views import api_detail_blog_view, api_update_blog_view, api_delete_blog_view, api_create_blog_view,api_list_blog_view,ApiBlogListViews
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', api_list_blog_view, name='blog-list'),
    path('<pk>/', api_detail_blog_view, name='detail'),
    path('<pk>/delete', api_delete_blog_view, name='delete'),
    path('<pk>/update', api_update_blog_view, name='update'),
    path('create', api_create_blog_view, name='create'),
    path('list', ApiBlogListViews.as_view(), name='list'),
]