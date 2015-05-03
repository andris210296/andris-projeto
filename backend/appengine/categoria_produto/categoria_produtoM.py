# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from google.appengine.ext.db import IntegerProperty
from gaeforms.base import Form, StringField, IntegerField
from gaeforms.ndb.form import ModelForm
from gaeforms.ndb.property import SimpleCurrency


class Categoria(ndb.Model):
    nomeCategoria = ndb.StringProperty(required=True)



    @classmethod
    def query_ordenada_por_nome(cls):
        return cls.query().order(Categoria.nomeCategoria)

class CategoriaForm(ModelForm):
    _model_class = Categoria


class Produto(ndb.Model):
    categoria_id = ndb.KeyProperty(required=True)
    nomeProduto = ndb.StringProperty(required=True)
    precoProduto = SimpleCurrency(required=True)


    @classmethod
    def query_ordenada_por_nome(cls):
        return cls.query().order(Produto.nomeProduto)


class ProdutoForm(ModelForm):
    _model_class = Produto