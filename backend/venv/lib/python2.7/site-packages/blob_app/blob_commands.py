# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import memcache

from google.appengine.api.blobstore import blobstore
from google.appengine.api.images import create_rpc, get_serving_url

from gaebusiness.business import Command, CommandParallel
from gaebusiness.gaeutil import ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, DestinationsSearch, CreateArc, DeleteArcs, NodeSearch, DeleteNode, \
    CreateSingleArc
from blob_app.blob_model import BlobFile, OwnerToBlob, img_with_size, IMG_CACHE_PREFIX
from gaegraph.model import destinations_cache_key, origins_cache_key


class BlobFileSaveForm(ModelForm):
    """
    Form used to save and update BlobFile
    """
    _model_class = BlobFile
    _include = [BlobFile.md5,
                BlobFile.filename,
                BlobFile.content_type,
                BlobFile.size]


class BlobFileForm(ModelForm):
    """
    Form used to expose BlobFile's properties for list or json
    """
    _model_class = BlobFile
    _exclude = [BlobFile.blob_key, BlobFile.img_url]

    def fill_with_model(self, model, img_size=32, *fields):
        dct = super(BlobFileForm, self).fill_with_model(model, *fields)
        dct['img'] = model.img(img_size)
        return dct


class SaveBlobFileCommand(Command):
    def __init__(self, blob_info):
        super(SaveBlobFileCommand, self).__init__()
        self.blob_info = blob_info
        self.__rpc = create_rpc(30)

    def set_up(self):
        try:
            get_serving_url(self.blob_info, rpc=self.__rpc, secure_url=True)
        except:
            pass  # If can not generate img url, there is nothing to do


    def do_business(self):
        blob_info = self.blob_info
        blob_file = BlobFile(filename=blob_info.filename, content_type=blob_info.content_type, size=blob_info.size,
                             md5=blob_info.md5_hash, blob_key=blob_info.key())
        try:
            blob_file.img_url = self.__rpc.get_result()
        except:
            pass  # there is nothing to do. Or it is not a image or it is greater than limit
        self._to_commit = blob_file
        self.result = blob_file


class SaveBlobFiles(CommandParallel):
    def __init__(self, *blob_infos):
        commands = [SaveBlobFileCommand(b) for b in blob_infos]
        super(SaveBlobFiles, self).__init__(*commands)

    def do_business(self):
        super(SaveBlobFiles, self).do_business()
        self.result = [cmd.result for cmd in self]


class CreateOwnerToBlob(CreateArc):
    arc_class = OwnerToBlob


class SaveBlobFilesWithOwner(CommandParallel):
    def __init__(self, owner, *blob_infos):
        commands = (SaveBlobFileCommand(b) for b in blob_infos)
        commands = [CreateOwnerToBlob(owner, cmd) for cmd in commands]
        super(SaveBlobFilesWithOwner, self).__init__(*commands)

    def do_business(self):
        super(SaveBlobFilesWithOwner, self).do_business()
        self.result = [cmd.destination for cmd in self]


class UpdateBlobFileCommand(UpdateNode):
    _model_form_class = BlobFileSaveForm


class ListBlobFileCommand(ModelSearchCommand):
    def __init__(self):
        super(ListBlobFileCommand, self).__init__(BlobFile.query_by_creation_desc())


class ListImagesCmd(Command):
    def __init__(self, size=32, owner=None, default=None):
        super(ListImagesCmd, self).__init__()
        self.default = default
        self.size = size
        if owner is None:
            self._cmd = ListBlobFileCommand()
            self._cache_key = IMG_CACHE_PREFIX + self._cmd._cache_key()
        else:
            self._cmd = ListBlobsFromOwnerCmd(owner)
            self._cache_key = IMG_CACHE_PREFIX + self._cmd._cache_key
        self.result = []

    def set_up(self):
        try:
            self.result = memcache.get(self._cache_key)
        except Exception:
            pass
        if not self.result:
            self._cmd.set_up()

    def do_business(self):
        if not self.result:
            self._cmd.do_business()
            result = self._cmd.result
            if result:
                self.result = [blob_file.img_url for blob_file in result]
                try:
                    memcache.set(self._cache_key, self.result)
                except:
                    pass
        self.result = [img_with_size(self.size, i) if i else self.default
                       for i in self.result]


class GetBlobFile(NodeSearch):
    _model_class = BlobFile


class _DeleteBlobFile(DeleteNode):
    _model_class = BlobFile


class ListBlobsFromOwnerCmd(DestinationsSearch):
    arc_class = OwnerToBlob


class DeleteOwnerToBlobArcs(DeleteArcs):
    arc_class = OwnerToBlob

    def do_business(self):
        super(DeleteOwnerToBlobArcs, self).do_business()

        if self.result:
            cache_keys = []
            if self._DeleteArcs__origin:
                cache_keys.append(IMG_CACHE_PREFIX + destinations_cache_key(self.arc_class, self._DeleteArcs__origin))
            else:
                for arc in self.result:
                    cache_keys.append(IMG_CACHE_PREFIX + destinations_cache_key(self.arc_class, arc.origin))

            if self._DeleteArcs__destination:
                cache_keys.append(IMG_CACHE_PREFIX + origins_cache_key(self.arc_class, self._DeleteArcs__destination))
            else:
                for arc in self.result:
                    cache_keys.append(IMG_CACHE_PREFIX + origins_cache_key(self.arc_class, arc.destination))
            memcache.delete_multi(cache_keys)


class DeleteBlobFiles(CommandParallel):
    def __init__(self, *model_keys):
        cmds = [DeleteOwnerToBlobArcs(destination=k) for k in model_keys]
        self.__delete_blob_cmds = [_DeleteBlobFile(k) for k in model_keys]
        cmds.extend(self.__delete_blob_cmds)
        super(DeleteBlobFiles, self).__init__(*cmds)

    def do_business(self):
        super(DeleteBlobFiles, self).do_business()
        blob_keys = [c.result.blob_key for c in self.__delete_blob_cmds]
        blobstore.delete(blob_keys)


class CreateSingleOwnerFile(CreateSingleArc):
    arc_class = OwnerToBlob