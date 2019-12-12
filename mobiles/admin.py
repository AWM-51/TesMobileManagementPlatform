# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from mobiles.models import User,Mobile
admin.site.register(User)
# Register your models here.
admin.site.register(Mobile)