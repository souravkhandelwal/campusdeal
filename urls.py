from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Django.views.home', name='home'),
    # url(r'^Django/', include('Django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^campusdeal/', include('campusdeal.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^campusdeal/home/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/item/\d+/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/myitems/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/next_recent/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/previous_recent/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/mybids/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/remove_bid/\d+/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/reg_submit/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/all/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/cycles/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/electronics/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/coolers/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/books/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/tickets/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/others/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
    (r'^campusdeal/search/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'D:/My Dropbox/acads/Code-A-Thon/Django/media/'}),
)
urlpatterns += staticfiles_urlpatterns()
