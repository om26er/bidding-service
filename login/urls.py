from django.conf.urls import url

from login import views

urlpatterns = [
    url(r'^users/$', views.UsersList.as_view()),
    url(r'^users/(?P<username>\w+)/$', views.UserDetail.as_view()),
    url(r'^user/$', views.UserExists.as_view())
]
