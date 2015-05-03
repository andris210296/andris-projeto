# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from categoria_produto.categoria_produtoM import ProdutoForm,Produto,Categoria
from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse

from tekton.gae.middleware.redirect import RedirectResponse


def salvarProduto(**campos):
    campos['categoria_id'] = ndb.Key(Categoria,int(campos['categoria_id']))
    produtoForm = ProdutoForm(**campos)
    erros = produtoForm.validate()

    if not erros:
        propriedades = produtoForm.normalize()
        novoProd = Produto(**propriedades)
        novoProd.put()

        from routes.andris import admin
        return RedirectResponse(admin)
    else:
        contexto = {'categoria_produto':campos,'erros':erros}
        return TemplateResponse(contexto,template_path='/andris/admin.html')