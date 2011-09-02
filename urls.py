import settings

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from security.profile.views import ProfileDisplayView

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),

	url(r'^profile/view/$', login_required(ProfileDisplayView.as_view())),

	url(r'^profile/view/(?P<user_id>\d+)/$',
		login_required(ProfileDisplayView.as_view())),

	(r'^media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': settings.MEDIA_ROOT}),
)
