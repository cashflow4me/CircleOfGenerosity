from listings import views
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from listings.models import Listing

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', views.home, name='home'),

    url(r'^listing/(\d+)/$', views.listing, name='listing'),

    url(r'^offers/$', views.listings_by_type,{'type':Listing.OFFER}, name='offers'),
    url(r'^offers/tag/(\d+)/$', views.listings_by_tag_id,{'type':Listing.OFFER}, name='offers'),
    url(r'^offers/tag/(\w+)/$', views.listings_by_tag_slug,{'type':Listing.OFFER}, name='offers'),

    url(r'^requests/$', views.listings_by_type,{'type':Listing.REQUEST}, name='requests'),
    url(r'^requests/tag/(\d+)/$', views.listings_by_tag_id, {'type':Listing.REQUEST}, name='requests'),
    url(r'^requests/tag/(\w+)/$', views.listings_by_tag_slug,{'type':Listing.REQUEST},  name='requests'),

    url(r'^post-listing/$',
        login_required(views.PostListingView.as_view()),
        name='post_listing'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name="login"),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('home')}, name="logout"),

    (r'^accounts/', include('allauth.urls')),

    url(r'^admin/', include(admin.site.urls)),
)