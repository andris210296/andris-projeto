# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from config.template_middleware import TemplateResponse
from gaepermission.decorator import permissions
from gaecookie.decorator import no_csrf
from categoria_produto.categoria_produtoM import Produto,Categoria
from permission_app.model import ADMIN
from google.appengine.ext import ndb
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from routes.andris.categoria_produto.salvarCategoria import salvarCategoria
from routes.andris.categoria_produto.salvarProduto import salvarProduto
from routes.andris.categoria_produto.editarCategoria import editarCategoria
from routes.andris.categoria_produto.editarProduto import editarProduto


#@permissions(ADMIN)
@no_csrf
def index():

    categoria_query = Categoria.query_ordenada_por_nome()
    produto_query = Produto.query_ordenada_por_nome()

    salvar_path = router.to_path(salvarCategoria)
    produto_salvar_path = router.to_path(salvarProduto)

    editar_path = router.to_path(editarCategoria)
    produto_editar_path = router.to_path(editarProduto)

    deletar_path= router.to_path(deletar)
    produto_deletar_path= router.to_path(deletarProduto)

    categorias = categoria_query.fetch()
    produtos = produto_query.fetch()

    for cat in categorias:
        cat_key = cat.key
        cat_key_id = cat_key.id()
        cat.editar_path = router.to_path(editar_path)
        cat.deletar_path = router.to_path(deletar_path, cat_key_id)

    for prod in produtos:
        prod_key = prod.key
        prod_key_id = prod_key.id()
        prod.editar_path = router.to_path(produto_editar_path)
        prod.deletar_path = router.to_path(produto_deletar_path, prod_key_id)


    contexto = {'categoria_lista':categorias,'produto_lista':produtos,'salvar_path':salvar_path,'produto_salvar_path':produto_salvar_path}
    return TemplateResponse(contexto,template_path='/andris/admin.html')

def deletar(categoria_id):
    key = ndb.Key(Categoria, int(categoria_id))
    key.delete()
    return RedirectResponse(index)

def deletarProduto(produto_id):
    key = ndb.Key(Produto, int(produto_id))
    key.delete()
    return RedirectResponse(index)






