# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Copyright 2012, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from json import loads
from neo4django.db import models


class Course(models.NodeModel):
    slug = models.StringProperty()
    description = models.StringProperty(null=True)

    @property
    def last_activity(self):
        return "NA"

    def last_info(self):
        dataset = self.courseinfo_set.all()
        data = dataset[0] if len(dataset) > 0 else CourseInfo(infos="[]")
        data.infos = loads(data.infos)
        return data


class CourseInfo(models.NodeModel):
    infos = models.StringProperty()
    date = models.DateTimeProperty(auto_now=True)
    course = models.Relationship(Course, rel_type='belongs_to')


class Category(models.NodeModel):
    slug = models.StringProperty()
    description = models.StringProperty(null=True)
