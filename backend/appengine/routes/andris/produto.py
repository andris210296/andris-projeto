# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from config.template_middleware import TemplateResponse
from routes.andris.categoria_produto.categoria_produtoM import *

@login_not_required
@no_csrf
def index(produto):


    produto = Produto.get_by_id(int(produto))



    query = Categoria.query_ordenada_por_nome()
    contexto = {'categoria_lista':query.fetch(),'crud':produto}

    return TemplateResponse(contexto,template_path='/andris/crud.html')

