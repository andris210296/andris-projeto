# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from google.appengine.ext.db import IntegerProperty
from gaeforms.base import Form, StringField, IntegerField
from gaeforms.ndb.form import ModelForm


class Categoria(ndb.Model):
    nomeCategoria = ndb.StringProperty(required=True)



    @classmethod
    def query_ordenada_por_nome(cls):
        return cls.query().order(Categoria.nomeCategoria)

class CategoriaForm(ModelForm):
    _model_class = Categoria
