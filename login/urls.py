from django.conf.urls import url

from login import views

urlpatterns = [
    # Register a new user and get list of users
    url(r'^users/$', views.UsersList.as_view()),
    # Get details for a specific user
    url(r'^users/(?P<username>\w+)/$', views.UserDetail.as_view()),
    # Get all ads by a user
    url(r'^users/(?P<username>\w+)/ads/$', views.UserAdsView.as_view()),
    url(r'^users/(?P<username>\w+)/ads/(?P<pk>[0-9]+)/$',
        views.UserAdView.as_view()),
    # Check if a user exists
    url(r'^user/$', views.UserExists.as_view()),
    # Get ad by requested filter
    url(r'^ad_filter/$', views.AdsView.as_view()),
    # Experimental push notifications sender
    url(r'^push/$', views.Push.as_view()),
]
