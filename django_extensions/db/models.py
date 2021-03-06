"""
Django Extensions abstract base model classes.
"""
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import (ModificationDateTimeField,
                                         CreationDateTimeField, AutoSlugField)

class TimeStampedModel(models.Model):
    """ TimeStampedModel
    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """
    created = CreationDateTimeField(_('created'))
    modified = ModificationDateTimeField(_('modified'))

    class Meta:
        abstract = True

class TitleSlugDescriptionModel(models.Model):
    """ TitleSlugDescriptionModel
    An abstract base class model that provides title and description fields
    and a self-managed "slug" field that populates from the title.
    """
    title = models.CharField(_('title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title')
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        abstract = True

class ActivatorModel(models.Model):
    """ ActivatorModel
    An abstract base class model that provides activate and deactivate fields.
    """
    STATUS_CHOICES = (
        (0, _('Inactive')),
        (1, _('Active')),
    )
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES,
        default=1)
    activate_date = models.DateTimeField(blank=True, null=True,
        help_text=_('keep empty for an immediate activation'))
    deactivate_date = models.DateTimeField(blank=True, null=True,
        help_text=_('keep empty for indefinite activation'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.activate_date:
            self.activate_date = datetime.datetime.now()
        super(ActivatorModel, self).save(*args, **kwargs)
