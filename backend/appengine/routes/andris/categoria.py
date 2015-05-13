# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from config.template_middleware import TemplateResponse
from categoria_produto.categoria_produtoM import Produto,Categoria
from tekton import router

@login_not_required
@no_csrf
def index(categoria):



    categoria = Categoria.get_by_id(int(categoria))

    categoria_query = Categoria.query_ordenada_por_nome().fetch()
    produto_query = Produto.query_por_categoria_ordenada_por_nome(categoria)
    produtos = produto_query.fetch()

    contexto = {'categoria_lista':categoria_query,'produto_lista':produtos,'categoria':categoria}

    return TemplateResponse(contexto,template_path='/andris/categoria.html')

