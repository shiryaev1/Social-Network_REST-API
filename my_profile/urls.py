from django.urls import path, re_path
from my_profile.views import *
from my_profile import views

urlpatterns = [
    path('', views.posts_list, name='posts_list_url'),
    path('post/create',PostCreate.as_view(), name='post_create_url'),
    re_path(r'^post/(?P<slug>[\w\-]+)/update/$', PostUpdate.as_view(),
            name='post_update_url'),
    re_path(r'^like/$',views.add_like, name='add_like'),
    re_path(r'^dislike/$',views.remove_like, name='remove_like'),
    path('tags/',views.tags_list, name='tags_list_url'),
    path('tag/create/',TagCreate.as_view(),name='tag_create_url'),
    re_path(r'^tag/(?P<slug>[\w\-]+)/$',TagDetail.as_view(),
            name='tag_detail_url'),
    re_path(r'^tag/(?P<slug>[\w\-]+)/update/$', TagUpdate.as_view(),
            name='tag_update_url'),
    re_path(r'^post/(?P<slug>[\w\-]+)/delete/$', PostDelete.as_view(),
            name='post_delete_url'),
    path('info/', views.profile_information, name='profile_information_url'),
    # path('edit/profile/', EditProfileInformation.as_view(), name='edit_profile'),
    re_path(r'^edit/profile/(?P<pk>\d+)/$', EditProfileInformation.as_view(),
            name='edit_profile_url'),
    path('profile/image', AddProfileImage.as_view(),
            name='add_profile_image_url'),
]