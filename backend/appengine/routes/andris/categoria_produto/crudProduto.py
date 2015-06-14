# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb

from routes.andris.categoria_produto.categoria_produtoM import ProdutoForm,Produto,Categoria
from distutils import log
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.json_middleware import JsonUnsecureResponse


@login_not_required
@no_csrf
def salvarProduto(_resp, **campos):


    campos['categoria_id'] = ndb.Key(Categoria,int(campos['categoria_id']))
    produtoForm = ProdutoForm(**campos)
    erros = produtoForm.validate()

    if erros:
        _resp.set_status(400)
        return JsonUnsecureResponse(erros)
    produto = produtoForm.fill_model()
    produto.put()
    dct = produtoForm.fill_with_model(produto)
    log.info(dct)
    return JsonUnsecureResponse(dct)



@login_not_required
@no_csrf
def editarProduto(_resp,**campos):
    produto = Produto.get_by_id(int(campos["produto_id"]))
    produto.nomeProduto = campos["nomeProduto"]
    produto.precoProduto = campos["precoProduto"]
    produto.put()
    dct = ProdutoForm().fill_with_model(produto)
    log.info(dct)
    return JsonUnsecureResponse(dct)


@login_not_required
@no_csrf
def listarProduto():
    produtos= Produto.query_ordenada_por_nome().fetch()
    produtos = [ProdutoForm().fill_with_model(prod) for prod in produtos]
    return JsonUnsecureResponse(produtos)

@login_not_required
@no_csrf
def deletarProduto(produto_id):
    key = ndb.Key(Produto, int(produto_id))
    key.delete()
