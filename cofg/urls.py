from listings import views
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', views.home, name='home'),

    url(r'^listing/(\d+)/$', views.listing, name='listing'),

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