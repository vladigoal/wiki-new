# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.http import HttpRequest

def cabinet_menu(request):
    path = request.META["PATH_INFO"]

    cabinet_menu = [{"name": "Профайл", "href": "profile/", "active": False}, {"name": "Мои заметки", "href": "notes/", "active": False}]
    for menu in cabinet_menu:
        if "/cabinet/%s"%menu["href"] == path:
            menu["active"] = True 

    return {"cabinet_menu": cabinet_menu}
