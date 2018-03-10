"""ph_dorms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from dorms import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('dorms/', include('dorms.urls')),
]

urlpatterns += [
	path('', RedirectView.as_view(url='/dorms/')),
]

urlpatterns	+= static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += [
	path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
	url(r'^$', RedirectView.as_view(url='/dorms/'), name='home'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^oauth/', include('social_django.urls', namespace='social')),
	url(r'^settings/$', core_views.settings, name='settings'),
	url(r'^settings/password/$', core_views.password, name='password'),
]