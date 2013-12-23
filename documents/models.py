# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Copyright 2012, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from neo4django.db import models as models
from www import settings


class Document(models.NodeModel):

    description = models.StringProperty()
    user = models.Relationship(settings.AUTH_USER_MODEL, rel_type='belongs_to')

    size = models.IntegerProperty(null=True, default=0)
    words = models.IntegerProperty(null=True, default=0)
    pages = models.IntegerProperty(null=True, default=0)
    date = models.DateTimeProperty(auto_now_add=True)

    views = models.IntegerProperty(null=True, default=0)
    downloads = models.IntegerProperty(null=True, default=0)

    staticfile = models.StringProperty(default='')
    source = models.StringProperty(default='')
    state = models.StringProperty(default='pending')

    def move(self, *args, **kwargs):
        # Must move a images and associated files
        # thus NotImplementedError
        raise NotImplementedError


class Page(models.NodeModel):
    numero = models.IntegerProperty()
    height_120 = models.IntegerProperty()
    height_600 = models.IntegerProperty()
    height_900 = models.IntegerProperty()

    def move(self, newparent):
        # You may not move a page from a document to another
        raise NotImplementedError
