# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from django.http import HttpResponse
import simplejson as json
import re

from manual.models import Item

def manual_view(request):
    template_name = "manual.html"

    try:
        logout = request.POST['logout']
    except:
        logout = None

    menuClass = multilevelMenu()
    
    items = Item.objects.all().order_by("id")
    menuClass.items = items


    response =  render_to_response('manual.html',
    {"username": request.COOKIES.get('username')},
    context_instance=RequestContext(request))
    if not request.COOKIES.get('sessionid'):
        response = redirect('/')
    if logout:
        response = redirect('/')
        response.delete_cookie('sessionid')
        response.delete_cookie('username')
    return response

menu_str = ""
menu_arr = []


class multilevelMenu:
    
    menu_dict = {} #menu full dict
    current_max_level = 0 #max level for current menu
    first_level_count = 0 #firs level menu count
    current_menu = 1 #current menu number, from menu_dict
    items = "" #all items with data
    used_ids = [] #items id, which used

    def first_level_func(self, id):
        for i in self.items:
            if i.parent_id == id:
                self.used_ids.append(i.id)
                self.menu_dict["menu1"]["level%s"%i.level] = {"name": i.name, "slug": i.slug}
        self.get_max_level(id)
        print "max_level=", self.current_max_level

    def get_max_level(self, id):
        for i in self.items:
            if i.parent_id == id:
                if(i.level >  self.current_max_level):
                    self.current_max_level = i.level
                    self.get_max_level(i.id)