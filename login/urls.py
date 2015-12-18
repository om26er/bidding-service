from django.conf.urls import url

from login import views

urlpatterns = [
    url(r'^users/$', views.UsersList.as_view()),
    url(r'^users/(?P<username>\w+)/$', views.UserDetail.as_view()),
    url(r'^users/(?P<username>\w+)/ads/$', views.UserAdsView.as_view()),
    url(r'^users/(?P<username>\w+)/ads/(?P<pk>[0-9]+)/$',
        views.UserAdView.as_view()),
    url(r'^user/$', views.UserExists.as_view()),
    url(r'^ad_filter/$', views.AdsView.as_view()),
    url(r'^push/$', views.Push.as_view()),
]
