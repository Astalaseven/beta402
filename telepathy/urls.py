# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Copyright 2014, Cercle Informatique ASBL. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This software was made by hast, C4, ititou at UrLab, ULB's hackerspace

from django.conf.urls import patterns, url
from telepathy.views import new_thread, show_thread, reply_thread


urlpatterns = patterns("",
    url(r"^put/$",
        new_thread,
        name="thread_put"),

    url(r"^reply/$",
        reply_thread,
        name="thread_reply"),

    url(r"^v/(?P<thread_id>[^/]*)/$",
        show_thread,
        name="thread_show"),
)
