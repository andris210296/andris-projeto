# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from config.template_middleware import TemplateResponse
from routes.andris.categoria_produto.categoria_produtoM import Produto,Categoria


@login_not_required
@no_csrf
def index(categoria):



    categoria = Categoria.get_by_id(int(categoria))

    categoria_query = Categoria.query_ordenada_por_nome()
    categorias = categoria_query.fetch()
    produto_query = Produto.query_por_categoria_ordenada_por_nome(categoria)
    produtos = produto_query.fetch()

    for cat in categorias:

        cat.QtdProd = len(Produto.query_por_categoria_ordenada_por_nome(Categoria.get_by_id(int(cat.key.id()))).fetch())

    contexto = {'categoria_lista':categorias,'produto_lista':produtos,'categoria_produto':categoria}

    return TemplateResponse(contexto,template_path='/andris/categoria_produto.html')

