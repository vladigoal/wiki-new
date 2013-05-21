# -*- coding: utf-8 -*-
from django.db import models
import datetime
from unidecode import unidecode
from django.template.defaultfilters import slugify
import re

def cur_date():
    return datetime.datetime.now().replace(microsecond=0)


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)
    
    current_slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug. Chop its length down if we need to.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create a queryset, excluding the current instance.
    if not queryset:
        queryset = instance.__class__._default_manager.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '-%s' % next
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)
    return slug

def _slug_strip(value, separator=None):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
        value = re.sub('%s+' % re_sep, separator, value)
    return re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)



class Item(models.Model):
    user_id = models.IntegerField(default = 0)
    name = models.CharField(max_length = 100, verbose_name = u'Заголовок')
    parent_id = models.IntegerField(default = 0, verbose_name = u'Родительский элемент')
    date = models.DateTimeField(null = True, default = cur_date, verbose_name = u'Дата')
    level = models.IntegerField(verbose_name = u'Уровень')
    type = models.IntegerField(verbose_name = u'Тип') #1-category, 2-article
    description = models.TextField(blank = True, verbose_name = u'Контент')
    slug = models.CharField(null = True, blank = True, max_length = 50)

    def save(self, **kwargs):
        self.slug = '%s' % (slugify(unidecode(u"%s"%self.name)))
        unique_slugify(self, self.slug)  ## from http://djangosnippets.org/snippets/1321/
        super(Item, self).save()

    def __unicode__(self):
        return self.name
