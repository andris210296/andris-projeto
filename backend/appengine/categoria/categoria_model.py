# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from google.appengine.ext.db import IntegerProperty
from gaeforms.base import Form, StringField, IntegerField
from gaeforms.ndb.form import ModelForm


class Categoria(ndb.Model):
    nome=ndb.StringProperty(required=True)
    quantidade=  ndb.IntegerProperty(required=True)
    criacao = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_ordenada_por_nome(cls):
        return cls.query().order(Categoria.nome)

class CategoriaForm(ModelForm):
    _model_class = Categoria
    _include = [Categoria.nome]
    quantidade=IntegerField(required=True,lower=0)