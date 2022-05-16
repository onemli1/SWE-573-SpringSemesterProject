from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blog.views import (
    create_blog_view,
    detail_post_view,
    edit_blog_view,
    like_post_view,
    unlike_post_view,
    show_category_page_view,
    show_space_page_view,
    create_space_view,
    remove_like_post_view,
    remove_unlike_post_view,
    create_comment_view,
    like_comment_view,
    unlike_comment_view,
    remove_like_comment_view,
    remove_unlike_comment_view,
    post_notification,
    delete_post_view,
)


urlpatterns = [
    path('create_post/', create_blog_view, name='create-post'),
    path('create_space/', create_space_view, name='create-space'),
    path('<slug>/', detail_post_view, name='detail-post'),
    path('<slug>/edit/', edit_blog_view, name='edit-post'),
    path('<slug>/delete/', delete_post_view, name='delete-post'),
    path('<slug>/like/', like_post_view, name='like-post'),
    path('<slug>/remove_like/', remove_like_post_view, name='remove-like-post'),
    path('<slug>/unlike/', unlike_post_view, name='unlike-post'),
    path('<slug>/remove_unlike/', remove_unlike_post_view, name='remove-unlike-post'),
    path('<slug>/comment/', create_comment_view, name='create-comment'),
    path("<slug>/<int:comment_id>/comment/like_comment", like_comment_view, name='like-comment'),
    path("<slug>/<int:comment_id>/comment/unlike_comment", unlike_comment_view, name='unlike-comment'),
    path("<slug>/<int:comment_id>/comment/remove_like_comment", remove_like_comment_view, name='remove-like-comment'),
    path("<slug>/<int:comment_id>/comment/remove_unlike_comment", remove_unlike_comment_view, name='remove-unlike-comment'),

    path("show_notification/<int:notification_pk>/<int:post_pk>/", post_notification, name='show-notification'),

    path('category/<str:category_name>', show_category_page_view, name='show_category'),
    path('space/<str:space_name>', show_space_page_view, name='show_space'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    