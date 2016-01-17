from django.conf.urls import url

from login import views

urlpatterns = [
    # Register a new user
    url(r'^api/register$', views.RegistrationView.as_view()),
    # get list of users. Admin access required
    url(r'^api/users/list$', views.UsersList.as_view()),
    # Get details for a specific user
    url(r'^api/users/(?P<username>\w+)/$', views.UserDetail.as_view()),
    # Get all ads by a user
    url(r'^api/users/(?P<username>\w+)/ads/post$',
        views.UserPostAdView.as_view()),
    # Get ads by a user
    url(r'^api/users/(?P<username>\w+)/ads/list$',
        views.UserAdsList.as_view()),
    # Get specific ad by a user
    url(r'^api/users/(?P<username>\w+)/ads/(?P<pk>[0-9]+)/$',
        views.UserAdView.as_view()),
    # Get and put user's interests. Requires user login.
    url(r'^api/users/(?P<username>\w+)/interests/$',
        views.InterestsView.as_view()),
    # Put user's push notification ID
    url(r'^api/users/(?P<username>\w+)/push_id$', views.PushKeyView.as_view()),
    # Check if a user exists
    url(r'^api/users/(?P<username>\w+)/exists$', views.UserExists.as_view()),
    # Get ad by requested filter
    url(r'^api/ads/$', views.AdsFilterView.as_view()),

    # Place a bid on an Ad
    url(r'^api/users/(?P<username>\w+)/ads/(?P<pk>[0-9]+)/bids/post',
        views.CreateBidView.as_view()),

    # Change/Delete/Retrieve a bid
    url(r'^api/users/(?P<username>\w+)/ads/(?P<ad_id>[0-9]+)/bids/'
        r'(?P<pk>[0-9]+)',
        views.GetUpdateDeleteBidView.as_view()),

    # # Get all the ads a user bid on
    # url(r'^api/users/(?P<username>\w+)/bids', views.UserBidsView.as_view()),

    # Get categories for the site
    url(r'^api/ads/categories$', views.CategoriesView.as_view()),
]
