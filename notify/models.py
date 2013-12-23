# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from neo4django.db import models
from www import settings

import signals

# 1. Event occurs in graph
# 2. Pre notif created
# 3. Notif daemon match against followers and create notif
# 4. User get notif and read it


class PreNotification(models.NodeModel):
    created = models.DateTimeProperty(auto_now=True)
    text = models.StringProperty(max_length=160)
    delivered = models.BooleanProperty(default=False)
    url = models.URLProperty()
    personal = models.BooleanProperty(default=False)

    user = models.Relationship(settings.AUTH_USER_MODEL, rel_type='created_by')  # The user that created the notification
    node = models.Relationship(models.NodeModel, rel_type='belongs_to')  # The node that initiated the notif

    def __str__(self):
        return self.text


class Notification(models.NodeModel):
    user = models.Relationship(settings.AUTH_USER_MODEL, rel_type='served_to')
    node = models.Relationship(models.NodeModel, rel_type='belongs_to')  # The effective node followed by user
    prenotif = models.Relationship(PreNotification, rel_type='source')
    read = models.BooleanProperty(default=False)

    @staticmethod
    def direct(user, text, node, url=None):
        """Directly deliver a single notification to a user"""
        Notification.objects.create(
            prenotif=PreNotification.objects.create(
                node=node,
                text=text,
                user=user,
                url=url,
                delivered=True,
                personal=True
            ),
            user=user,
            node=node
        )

    @staticmethod
    def unread(user):
        """Return all unread notifications for user"""
        return Notification.objects.filter(user=user, read=False)


post_save.connect(signals.pre_notif_save, sender=PreNotification)
