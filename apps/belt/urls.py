from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index, name = 'index'),
    url(r'^login$', login, name='login'),
    url(r'^register$', register, name ='register'),
    url(r'^home$', home, name='home'),
    url(r'^process/(?P<quotes_id>\d+)$', process, name='process'),
    url(r'^create$', create, name='create'),
    url(r'^user/(?P<user_id>\d+)$', userPage, name='user'),
    url(r'^logout', logout, name='logout'),
    url(r'^remove/(?P<quotes_id>\d+)$', remove, name='remove')
]
