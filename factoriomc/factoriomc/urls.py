from channels.routing import include as include_chan
from channels.routing import route
from core.consumers import (admin_connected, admin_disconnected, admin_message,
                            server_connected, server_disconnected,
                            server_message)
from core.views import IndexView, ServerDebugView
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^serverdebug/(?P<pk>[0-9]+)/$', staff_member_required(ServerDebugView.as_view()), name='serverdebug'),
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

    route("websocket.connect", admin_connected,
          path=r"^/$"),
    route("websocket.receive", admin_message,
          path=r"^/$"),
    route("websocket.disconnect", admin_disconnected,
          path=r"^/$"),
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
