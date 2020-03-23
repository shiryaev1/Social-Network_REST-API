from django.urls import path, re_path
from my_profile.views import *
from my_profile import views

urlpatterns = [
    path('', views.posts_list, name='posts_list_url'),
    path('profile/', ViewProfile.as_view(), name='profile'),
    re_path(r'^post/(?P<id>\d+)/update/$', PostUpdate.as_view(),
            name='post_update_url'),
    # path('profile/edit', views.user_photos_view, name='edit-profile'),
    re_path(r'^like/$',views.add_like, name='add_like'),
    re_path(r'^dislike/$',views.remove_like, name='remove_like'),
    re_path(r'^post/(?P<id>\d+)/delete/$', PostDelete.as_view(),
            name='post_delete_url'),
    path('info/', views.profile_information, name='profile_information_url'),
    re_path(r'^profile/edit/(?P<pk>\d+)/$', EditProfileInformation.as_view(),
            name='edit_profile_url'),
    path('profile/image', AddProfileImage.as_view(),
            name='add_profile_image_url'),
    path('profile/peoples', views.peoples, name='peoples'),
    re_path(r'^people/(?P<pk>\d+)/profile/$', PeopleViewProfile.as_view(),
            name='people-profile'),
    re_path(r'^click/(?P<pk>\d+)/$', click_on_the_contact,
            name='click'),

]