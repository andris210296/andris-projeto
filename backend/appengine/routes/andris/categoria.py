# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from config.template_middleware import TemplateResponse
from categoria_produto.categoria_produtoM import *
from tekton import router

@login_not_required
@no_csrf
def index(categoria):
    query = Categoria.query_ordenada_por_nome()
    contexto = {'categoria_lista':query.fetch(),'categoria_produto':categoria}
    return TemplateResponse(contexto,template_path='andris/categoria_produto.html')

