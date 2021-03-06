from django.conf.urls.defaults import patterns, include
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^require/', include('qualitio.requirements.urls')),
                       (r'^report/', include('qualitio.report.urls')),
                       (r'^settings/', include('qualitio.projects.urls')),
                       (r'^execute/', include('qualitio.execute.urls')),
                       (r'^store/', include('qualitio.store.urls')),

                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       )

urlpatterns += patterns('django.views.generic.simple',
                        ('^$', 'redirect_to', {'url': 'require/'}),
                        )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                            )
