#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .views import AdminHandler, CubeHandler, ConnectionHandler
from .views import ElementHandler, DashboardHandler, APICubeHandler


INCLUDE_URLS = [
    (r"/admin", AdminHandler),
    (r"/admin/connection", ConnectionHandler),
    (r"/admin/cube/?(?P<slug>[\w-]+)?", CubeHandler),
    (r"/admin/api/cube/?(?P<slug>[\w-]+)?", APICubeHandler),
    (r"/admin/element/?(?P<slug>[\w-]+)?", ElementHandler),
    (r"/admin/dashboard/?(?P<slug>[\w-]+)?", DashboardHandler),
]