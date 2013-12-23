# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Copyright 2012, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from neo4django.db import models
from neo4django.graph_auth.models import User, UserManager

from graph.models import Course
from django.db.models import Q
import re


class MyUser(User):

    USERNAME_FIELD = 'netid'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    DEFAULT_PHOTO = "/static/profile/default.jpg"
    objects = UserManager()

    netid = models.StringProperty(indexed=True, unique=True, null=False, blank=False)
    registration = models.StringProperty()
    photo = models.StringProperty(default="")
    welcome = models.BooleanProperty(default=True)
    comment = models.StringProperty(null=True)

    follow = models.Relationship('polydag.Node', rel_type='follows')

    def get_username(self):
        return self.netid

    @property
    def get_photo(self):
        photo = self.DEFAULT_PHOTO
        if self.photo != "":
            photo = "/static/profile/{0.netid}.{0.photo}".format(self)

        return photo

    @property
    def name(self):
        return "{0.first_name} {0.last_name}".format(self)

    def directly_followed(self):
        return self.follow.all()

    def followed_nodes_id(self):
        try:
            self.followed_cache
        except:
            direct = self.follow.only('id').non_polymorphic()
            direct_descendants = map(lambda x: x.descendants_set(True), direct)
            indirect = reduce(lambda x, y: x | y, direct_descendants, set())
            indirect_ids = map(lambda x: x.id, indirect)
            self.followed_cache = indirect_ids
        return self.followed_cache

    def followed_courses(self):
        ids = self.followed_nodes_id()
        if len(ids) > 0:
            qs = map(lambda x: Q(id=x), ids)
            q = reduce(lambda x, y: x | y, qs)
            return Course.objects.filter(q)
        else:
            return []


class Inscription(models.NodeModel):
    user = models.Relationship('polydag.Node', rel_type='belongs_to')
    faculty = models.StringProperty(null=True)
    section = models.StringProperty(null=True)
    year = models.IntegerProperty(null=True)

    class Meta:
        unique_together = ('user', 'section', 'faculty', 'year')

    @property
    def level(self):
        place = re.search('\d', self.section)
        if place:
            return int(self.section[place.start()])
        else:
            return None

    @property
    def type(self):
        place = re.search('\d', self.section)
        if place:
            return self.section[:place.start()]
        else:
            return self.section

    @property
    def next(self):
        next_starts = "{}{}".format(self.type, self.level + 1)
        # TODO : should use category slugs and not Inscriptions
        return Inscription.objects.filter(section__startswith=next_starts)
