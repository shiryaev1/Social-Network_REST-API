from django.urls import path, re_path
from django.contrib.auth.views import (
	LoginView, LogoutView,
)
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='posts_list_url'),
         name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    re_path(r'^profile/(?P<pk>\d+)/$', views.view_profile,
            name='view_profile_with_pk'),
    re_path(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends,
            name='change_friends')
]
