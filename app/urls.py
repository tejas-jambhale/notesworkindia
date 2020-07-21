from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [	
    #WEBAPP url
    url(r'^$', views.signup, name='login'),
    url(r'^user/auth/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^sites/$', login_required(views.AddView),  name='createnotes'),
    url(r'^sites/list/$', views.ListView.as_view()),
    url(r'^sites/list/(?P<pk>[0-9a-f-]+)/$', views.NotesView.as_view()),
   


   ] 