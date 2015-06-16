# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import memcache

from google.appengine.ext import ndb

from gaegraph.model import Node, Arc, origins_cache_key, destinations_cache_key


def img_with_size(size, img_url):
    if img_url and size:
        return '%s=s%s' % (img_url, size)
    return img_url if img_url else ''


class BlobFile(Node):
    filename = ndb.StringProperty(required=True)
    content_type = ndb.StringProperty(required=True)
    size = ndb.IntegerProperty(required=True)
    md5 = ndb.StringProperty(required=True)
    blob_key = ndb.BlobKeyProperty(required=True)

    img_url = ndb.TextProperty(default=None)  # Used only for images

    def img(self, size=None):
        return img_with_size(size, self.img_url)


IMG_CACHE_PREFIX = 'img'


class OwnerToBlob(Arc):
    destination = ndb.KeyProperty(BlobFile)

    @classmethod
    def default_order(cls):
        return -cls.creation

    def _pre_put_hook(self):
        if hasattr(self, 'key'):
            origins_key = origins_cache_key(self.__class__, self.destination)
            destinations_key = destinations_cache_key(self.__class__, self.origin)
            keys = [origins_key, destinations_key, IMG_CACHE_PREFIX + origins_key, IMG_CACHE_PREFIX + destinations_key]
            memcache.delete_multi(keys)





