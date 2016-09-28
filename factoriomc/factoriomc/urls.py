"""factoriomc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from channels.routing import include as include_chan
from channels.routing import route
from core.consumers import (server_connected, server_disconnected,
                            server_message)
from django.conf.urls import include, url
from django.contrib import admin
from core.views import IndexView, ServerDebugView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^serverdebug/(?P<pk>[0-9]+)/$', ServerDebugView.as_view(), name='serverdebug'),
    url(r'^admin/', include(admin.site.urls)),
]

ws_routing = [
    # Capture all /resource/id/ requests
    route("websocket.connect", server_connected,
          path=r"^/server_callback/(?P<pk>[0-9]+)/$"),
    route("websocket.receive", server_message,
          path=r"^/server_callback/(?P<pk>[0-9]+)/$"),
    route("websocket.disconnect", server_disconnected,
          path=r"^/server_callback/(?P<pk>[0-9]+)/$"),
]

#task_routing = [
    #route('create-project', create_project),
#]

channel_routing = [
    # Namespace this in case we want something completely different in the
    # future.
    include_chan(ws_routing, path=r"^/ws_v1"),
    #include_chan(task_routing),
]
