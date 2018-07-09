from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.db import models
from django.utils.encoding import force_text
from django.contrib import messages
from django.contrib.messages import utils
from django.utils.translation import ugettext_lazy as _

import persistent_messages
from persistent_messages.constants import PERSISTENT_MESSAGE_LEVELS


LEVEL_TAGS = utils.get_level_tags()
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Message(models.Model):
    LEVEL_CHOICES = (
        (messages.DEBUG, 'DEBUG'),
        (messages.INFO, 'INFO'),
        (messages.SUCCESS, 'SUCCESS'),
        (messages.WARNING, 'WARNING'),
        (messages.ERROR, 'ERROR'),
        (persistent_messages.DEBUG, 'PERSISTENT DEBUG'),
        (persistent_messages.INFO, 'PERSISTENT INFO'),
        (persistent_messages.SUCCESS, 'PERSISTENT SUCCESS'),
        (persistent_messages.WARNING, 'PERSISTENT WARNING'),
        (persistent_messages.ERROR, 'PERSISTENT ERROR'),
    )

    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    from_user = models.ForeignKey(AUTH_USER_MODEL, blank=True, null=True,
        related_name="from_user", on_delete=models.SET_NULL)
    subject = models.CharField(max_length=255, blank=True, default='')
    message = models.TextField()
    level = models.IntegerField(choices=LEVEL_CHOICES)
    extra_tags = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)    
    modified = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    expires = models.DateTimeField(null=True, blank=True)
    close_timeout = models.IntegerField(null=True, blank=True)

    def is_persistent(self):
        return self.level in PERSISTENT_MESSAGE_LEVELS
    is_persistent.boolean = True
    
    def __eq__(self, other):
        return isinstance(other, Message) and self.level == other.level and \
                                              self.message == other.message
    def __str__(self):
        if self.subject:
            message = '{}: {}'.format(self.subject, self.message)
        else:
            message = self.message
        return force_text(message)

    def _prepare_message(self):
        """
        Prepares the message for saving by forcing the ``message``
        and ``extra_tags`` and ``subject`` to unicode in case they are lazy translations.

        Known "safe" types (None, int, etc.) are not converted (see Django's
        ``force_text`` implementation for details).
        """
        self.subject = force_text(self.subject, strings_only=True)
        self.message = force_text(self.message, strings_only=True)
        self.extra_tags = force_text(self.extra_tags, strings_only=True)

    def save(self, *args, **kwargs):
        self._prepare_message()
        super(Message, self).save(*args, **kwargs)

    @property
    def tags(self):
        label_tag = force_text(LEVEL_TAGS.get(self.level, ''), strings_only=True)
        extra_tags = force_text(self.extra_tags, strings_only=True)
        read_tag = "read" if self.read else "unread"
   
        if extra_tags and label_tag:
            return u' '.join([extra_tags, label_tag, read_tag])
        elif extra_tags:
            return u' '.join([extra_tags, read_tag])
        elif label_tag:
            return u' '.join([label_tag, read_tag])
        return read_tag

